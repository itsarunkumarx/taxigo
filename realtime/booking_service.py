"""
Booking service for Taxigo — handles driver search, assignment, and status transitions.
Called from booking views and WebSocket consumers.
"""

import asyncio
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

from .cache import driver_location_cache, booking_lock_cache, ride_request_cache

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()


def find_and_notify_drivers(booking_id: str, lat: float, lng: float,
                             vehicle_type: str, fare: float, distance_km: float):
    """
    Geospatial driver search with expanding radius.
    Sends ride request to top 3 nearest available drivers.
    Returns list of driver_ids notified, or [] if none found.
    """
    radii = getattr(settings, "DRIVER_SEARCH_RADII_KM", [2, 5, 8, 10])

    for radius_km in radii:
        nearby = driver_location_cache.find_nearby_drivers(lat, lng, radius_km)

        # Filter only verified + available drivers (DB check done in booking view before calling this)
        if not nearby:
            logger.info(f"[BookingService] No drivers found within {radius_km}km — expanding...")
            continue

        # Take top 3
        top_3 = nearby[:3]
        driver_ids = [d["driver_id"] for d in top_3]

        # Store pending drivers in Redis
        ride_request_cache.set_pending_drivers(booking_id, driver_ids)

        # Broadcast ride request to each driver's WebSocket channel
        for driver_data in top_3:
            did = driver_data["driver_id"]
            try:
                async_to_sync(channel_layer.group_send)(
                    f"driver_requests_{did}",
                    {
                        "type":         "ride_request",
                        "booking_id":   str(booking_id),
                        "pickup_lat":   lat,
                        "pickup_lng":   lng,
                        "vehicle_type": vehicle_type,
                        "fare":         fare,
                        "distance_km":  distance_km,
                        "dist_to_pickup": driver_data["distance_km"],
                        "timeout":      getattr(settings, "DRIVER_REQUEST_TIMEOUT", 15),
                    }
                )
                logger.info(f"[BookingService] Sent ride request to driver {did}")
            except Exception as e:
                logger.warning(f"[BookingService] Failed to notify driver {did}: {e}")

        return driver_ids

    # No drivers found in any radius
    logger.warning(f"[BookingService] No drivers found for booking {booking_id}")
    _mark_no_driver(booking_id)
    return []


def broadcast_booking_status(booking_id: str, status: str, extra: dict = None):
    """
    Broadcast status update to the booking's WebSocket group (customer listens here).
    """
    payload = {
        "type":       "booking_status",
        "booking_id": str(booking_id),
        "status":     status,
    }
    if extra:
        payload.update(extra)
    try:
        async_to_sync(channel_layer.group_send)(f"booking_{booking_id}", payload)
    except Exception as e:
        logger.warning(f"[BookingService] Broadcast failed for {booking_id}: {e}")


def _mark_no_driver(booking_id: str):
    """Update booking status in DB to NO_DRIVER_FOUND."""
    try:
        from booking.models import Booking
        Booking.objects.filter(id=booking_id).update(status="NO_DRIVER_FOUND")
        broadcast_booking_status(booking_id, "NO_DRIVER_FOUND")
    except Exception as e:
        logger.error(f"[BookingService] Could not mark no-driver: {e}")


def log_ride_event(booking_id: str, event_type: str, actor_id: str = "",
                   actor_role: str = "SYSTEM", lat=None, lng=None, meta: dict = None):
    """Write an immutable ride log entry."""
    try:
        from realtime.models import RideLog
        RideLog.objects.create(
            booking_id=str(booking_id),
            event_type=event_type,
            actor_id=actor_id,
            actor_role=actor_role,
            lat=lat,
            lng=lng,
            metadata=meta or {},
        )
    except Exception as e:
        logger.warning(f"[RideLog] Could not write log: {e}")
