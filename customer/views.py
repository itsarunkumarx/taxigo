from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from booking.models import Booking

@login_required(login_url="login")
def customer_dashboard(request):

    bookings = Booking.objects.filter(customer=request.user)

    context = {
        "total_bookings": bookings.count(),
        "pending": bookings.filter(status="Pending").count(),
        "completed": bookings.filter(status="Completed").count(),
        "cancelled": bookings.filter(status="Cancelled").count(),
    }

    return render(request, "customer/dashboard.html", context)