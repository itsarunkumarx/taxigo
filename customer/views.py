from django.shortcuts import render
from accounts.decorators import role_required
from booking.models import Booking

@role_required("CUSTOMER")
def customer_dashboard(request):

    bookings = Booking.objects.filter(customer=request.user)

    context = {
        "total_bookings": bookings.count(),
        "pending": bookings.filter(status="Pending").count(),
        "completed": bookings.filter(status="Completed").count(),
        "cancelled": bookings.filter(status="Cancelled").count(),
    }

    return render(request, "customer/dashboard.html", context)