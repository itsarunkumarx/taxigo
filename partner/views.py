from django.db.models import Sum

from accounts.decorators import role_required
from django.shortcuts import render

from vehicle.models import Vehicle
from driver.models import Driver
from booking.models import Booking
from payment.models import Payment


@role_required("PARTNER")
def partner_dashboard(request):

    vehicles = Vehicle.objects.filter(owner=request.user)
    drivers = Driver.objects.filter(partner=request.user)
    bookings = Booking.objects.filter(vehicle__owner=request.user)

    earnings = Payment.objects.filter(
        booking__vehicle__owner=request.user,
        payment_status="Paid"
    ).aggregate(total=Sum("amount"))["total"] or 0

    context = {
        "vehicle_count": vehicles.count(),
        "available_vehicle_count": vehicles.filter(is_available=True).count(),
        "driver_count": drivers.count(),
        "active_driver_count": drivers.filter(status="Active").count(),
        "booking_count": bookings.count(),
        "pending_count": bookings.filter(status="Pending").count(),
        "completed_count": bookings.filter(status="Completed").count(),
        "total_earnings": earnings,
        "recent_bookings": bookings.order_by("-id")[:5],
    }

    return render(request, "partner/dashboard.html", context)
