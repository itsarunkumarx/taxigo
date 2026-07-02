from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import CustomUser
from vehicle.models import Vehicle
from booking.models import Booking
from payment.models import Payment


@login_required
def admin_dashboard(request):

    customer_count = CustomUser.objects.filter(role="CUSTOMER").count()

    owner_count = CustomUser.objects.filter(role="OWNER").count()

    driver_count = CustomUser.objects.filter(role="DRIVER").count()

    vehicle_count = Vehicle.objects.count()

    booking_count = Booking.objects.count()

    payment_count = Payment.objects.count()

    available_vehicle = Vehicle.objects.filter(
        is_available=True
    ).count()

    context = {
        "customer_count": customer_count,
        "owner_count": owner_count,
        "driver_count": driver_count,
        "vehicle_count": vehicle_count,
        "booking_count": booking_count,
        "payment_count": payment_count,
        "available_vehicle": available_vehicle,
    }

    return render(
        request,
        "admin/dashboard.html",
        context,
    )