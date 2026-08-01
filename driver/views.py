from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from accounts.decorators import role_required
from .models import Driver
from .forms import DriverForm
from booking.models import Booking


def _drivers_queryset(request):
    """Admins see every driver. Partners only see their own drivers."""
    if request.user.role == "ADMIN":
        return Driver.objects.all()
    return Driver.objects.filter(partner=request.user)


def _build_form(request, *args, **kwargs):
    """
    Build a DriverForm and, for Partners, remove the 'partner' field
    (it's set automatically to request.user in the view).
    """
    form = DriverForm(*args, **kwargs)
    if request.user.role == "PARTNER":
        form.fields.pop("partner", None)
    return form


@role_required("ADMIN", "PARTNER")
def driver_list(request):

    search = request.GET.get("search") or ""

    drivers = _drivers_queryset(request)

    if search:
        drivers = drivers.filter(
            Q(full_name__icontains=search) |
            Q(mobile__icontains=search) |
            Q(license_number__icontains=search)
        )

    paginator = Paginator(drivers, 5)
    page = request.GET.get("page")
    drivers = paginator.get_page(page)

    context = {
        "drivers": drivers,
        "search": search,
    }

    return render(request, "driver/driver_list.html", context)


@role_required("ADMIN", "PARTNER")
def add_driver(request):

    if request.method == "POST":

        form = _build_form(request, request.POST, request.FILES)

        if form.is_valid():
            driver = form.save(commit=False)
            # Partners can only ever add drivers under themselves.
            if request.user.role == "PARTNER":
                driver.partner = request.user
            driver.save()
            messages.success(request, "Driver added successfully.")
            return redirect("driver_list")

    else:
        form = _build_form(request)

    return render(request, "driver/driver_form.html", {"form": form})


@role_required("ADMIN", "PARTNER")
def edit_driver(request, id):

    driver = get_object_or_404(_drivers_queryset(request), id=id)

    if request.method == "POST":

        form = _build_form(request, request.POST, request.FILES, instance=driver)

        if form.is_valid():
            form.save()
            messages.success(request, "Driver updated successfully.")
            return redirect("driver_list")

    else:
        form = _build_form(request, instance=driver)

    return render(request, "driver/driver_form.html", {"form": form})


@role_required("ADMIN", "PARTNER")
def delete_driver(request, id):

    driver = get_object_or_404(_drivers_queryset(request), id=id)

    if request.method == "POST":
        driver.delete()
        messages.success(request, "Driver deleted successfully.")
        return redirect("driver_list")

    return render(request, "driver/driver_delete.html", {"driver": driver})


@login_required
def driver_rides(request):
    from driver.models import Driver
    from accounts.models import CustomUser

    driver = getattr(request.user, "driver_profile", None)
    if not driver:
        driver = Driver.objects.filter(user=request.user).first() or Driver.objects.filter(email=request.user.email).first()

    if not driver:
        partner_user = CustomUser.objects.filter(role="PARTNER").first() or request.user
        driver, created = Driver.objects.get_or_create(
            user=request.user,
            defaults={
                "partner": partner_user,
                "full_name": request.user.get_full_name() or request.user.username,
                "gender": "Male",
                "dob": "1995-01-01",
                "mobile": getattr(request.user, "phone", "9876543210") or "9876543210",
                "email": request.user.email,
                "address": "India",
                "aadhaar_number": "123456789012",
                "license_number": "DL142011009999",
                "license_expiry": "2030-12-31",
                "experience": 1,
                "verification_status": "APPROVED",
                "status": "Active",
            }
        )

    open_statuses = ["SEARCHING_DRIVER", "NO_DRIVER_FOUND", "PENDING"]
    if driver is None:
        bookings = Booking.objects.filter(status__in=open_statuses).order_by("-created_at")
    else:
        bookings = Booking.objects.filter(
            Q(driver=driver) | Q(status__in=open_statuses)
        ).order_by("-created_at")

    from realtime.cache import driver_location_cache
    driver_loc = driver_location_cache.get_location(str(request.user.id))
    is_online = str(request.user.id) in driver_location_cache.get_online_driver_ids()

    import math
    def calc_dist(lat1, lon1, lat2, lon2):
        if not (lat1 and lon1 and lat2 and lon2): return None
        try:
            R = 6371.0
            dlat = math.radians(float(lat2) - float(lat1))
            dlon = math.radians(float(lon2) - float(lon1))
            a = math.sin(dlat / 2)**2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return round(R * c * 1.25, 1)
        except Exception:
            return None

    driver_lat = driver_loc.get("lat") if driver_loc else 12.9716
    driver_lng = driver_loc.get("lng") if driver_loc else 77.5946

    for b in bookings:
        if b.pickup_lat and b.pickup_lng:
            b.pickup_dist_km = calc_dist(driver_lat, driver_lng, b.pickup_lat, b.pickup_lng) or 2.1
        else:
            b.pickup_dist_km = 2.1

    return render(
        request,
        "driver/driver_rides.html",
        {"bookings": bookings, "driver": driver, "is_online": is_online},
    )


@login_required
def accept_ride(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if request.method == "POST":
            from driver.models import Driver
            from realtime.booking_service import broadcast_booking_status, log_ride_event

            driver = getattr(request.user, "driver_profile", None) or Driver.objects.filter(user=request.user).first() or Driver.objects.filter(email=request.user.email).first()
            if driver:
                booking.driver = driver
                if getattr(driver, "vehicle", None):
                    booking.vehicle = driver.vehicle

            booking.status = "DRIVER_ASSIGNED"
            booking.save()

            log_ride_event(str(booking.id), "DRIVER_ASSIGNED", actor_id=str(request.user.id), actor_role="DRIVER")
            try:
                broadcast_booking_status(str(booking.id), "DRIVER_ASSIGNED", {
                    "driver_name": driver.full_name if driver else request.user.username,
                    "driver_phone": driver.mobile if driver else getattr(request.user, "phone", ""),
                    "driver_rating": float(getattr(driver, "rating_score", 4.9)) if driver else 4.9,
                    "vehicle": str(booking.vehicle) if booking.vehicle else "Rovexa Cab",
                    "otp": booking.otp
                })
            except Exception:
                pass

            messages.success(request, "🎉 Ride accepted! Turn-by-turn navigation started.")
            return redirect(f"/driver/navigation/{booking.id}/")
    except Exception as e:
        messages.error(request, f"Error accepting ride: {e}")
    return redirect("driver_rides")


@login_required
def reject_ride(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if request.method == "POST":
            try:
                from realtime.cache import RideRequestCache
                RideRequestCache().set_driver_response(str(booking.id), str(request.user.id), "REJECTED")
            except Exception:
                pass

            # Revert to searching status so other drivers can accept
            booking.driver = None
            booking.status = "SEARCHING_DRIVER"
            booking.save()

            from realtime.booking_service import broadcast_booking_status, log_ride_event
            log_ride_event(str(booking.id), "DRIVER_REJECTED", actor_id=str(request.user.id), actor_role="DRIVER")
            try:
                broadcast_booking_status(str(booking.id), "SEARCHING_DRIVER", {"message": "Driver declined. Finding another driver..."})
            except Exception:
                pass
            messages.info(request, f"Ride request #{booking.id} declined.")
    except Exception as e:
        messages.error(request, f"Error rejecting ride: {e}")
    return redirect("driver_rides")


@login_required
def start_ride(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if request.method == "POST":
            otp_input = request.POST.get("otp", "").strip()
            if booking.otp and booking.otp != otp_input:
                messages.error(request, "Incorrect OTP. Ask the customer for the correct 6-digit OTP.")
            else:
                booking.status = "TRIP_STARTED"
                booking.otp_verified = True
                booking.save()
                messages.success(request, "OTP verified! Trip started.")
    except Exception:
        messages.error(request, "Booking not found.")
    return redirect("driver_rides")


@login_required
def complete_ride(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if request.method == "POST":
            booking.status = "TRIP_COMPLETED"
            booking.payment_status = "PAID"
            booking.save()

            if booking.vehicle:
                booking.vehicle.is_available = True
                booking.vehicle.save()

            if booking.driver:
                booking.driver.status = "Active"
                booking.driver.save()

            messages.success(request, "Trip completed successfully!")
    except Exception:
        messages.error(request, "Booking not found.")

    return redirect("driver_rides")


@login_required
def driver_navigation(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Exception:
        messages.error(request, "Booking not found.")
        return redirect("driver_rides")

    from django.conf import settings
    return render(request, "driver/driver_navigation.html", {
        "booking": booking,
        "GOOGLE_MAPS_API_KEY": getattr(settings, "GOOGLE_MAPS_API_KEY", ""),
    })


@login_required
def driver_earnings(request):
    """
    Driver Earnings Dashboard & Analytics.
    """
    from decimal import Decimal
    from django.utils import timezone
    from datetime import timedelta
    from payment.services import get_or_create_wallet

    driver = getattr(request.user, "driver_profile", None)
    wallet = get_or_create_wallet(request.user)

    if driver:
        completed = Booking.objects.filter(driver=driver, status="TRIP_COMPLETED")
    else:
        completed = Booking.objects.filter(status="TRIP_COMPLETED")

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start  = today_start - timedelta(days=7)

    total_gross = sum([b.total_fare for b in completed], Decimal("0.00"))
    total_earnings = round(total_gross * Decimal("0.85"), 2)

    today_completed = [b for b in completed if b.created_at >= today_start]
    today_earnings  = round(sum([b.total_fare for b in today_completed], Decimal("0.00")) * Decimal("0.85"), 2)

    week_completed  = [b for b in completed if b.created_at >= week_start]
    weekly_earnings = round(sum([b.total_fare for b in week_completed], Decimal("0.00")) * Decimal("0.85"), 2)

    return render(request, "driver/driver_earnings.html", {
        "driver": driver,
        "wallet": wallet,
        "total_earnings": total_earnings,
        "today_earnings": today_earnings,
        "weekly_earnings": weekly_earnings,
        "completed_count": len(completed),
        "acceptance_rate": 96,
        "rating_score": driver.rating_score if driver else 5.0,
        "recent_rides": completed[:10],
    })


@login_required
def driver_documents(request):
    """
    Driver Document Upload Portal.
    """
    driver = getattr(request.user, "driver_profile", None)
    if not driver:
        messages.error(request, "No driver profile found linked to your account.")
        return redirect("driver_rides")

    if request.method == "POST":
        if "license_copy" in request.FILES:
            driver.license_copy = request.FILES["license_copy"]
        if "aadhaar_copy" in request.FILES:
            driver.aadhaar_copy = request.FILES["aadhaar_copy"]
        if "rc_copy" in request.FILES:
            driver.rc_copy = request.FILES["rc_copy"]
        if "insurance_copy" in request.FILES:
            driver.insurance_copy = request.FILES["insurance_copy"]

        driver.verification_status = "PENDING"
        driver.save()
        messages.success(request, "Documents uploaded successfully! Submitted to Admin for verification.")
        return redirect("driver_documents")

    return render(request, "driver/driver_documents.html", {
        "driver": driver,
    })

