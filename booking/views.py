from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from vehicle.models import Vehicle
from .models import Booking
from .forms import BookingForm


# ===============================
# Booking List
# ===============================
@login_required
def booking_list(request):

    bookings = Booking.objects.select_related(
        "customer",
        "vehicle",
        "driver"
    ).order_by("-id")

    return render(
        request,
        "booking/booking_list.html",
        {
            "bookings": bookings
        }
    )


# ===============================
# Add Booking
# ===============================
@login_required
def add_booking(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            # Logged-in customer
            booking.customer = request.user

            # Distance from hidden field
            distance = request.POST.get("distance", "0")

            try:
                booking.distance = Decimal(distance)
            except:
                booking.distance = Decimal("0")

            # Calculate fare automatically
            if booking.vehicle:

                booking.total_fare = (
                    booking.distance *
                    booking.vehicle.price_per_km
                )

            else:

                booking.total_fare = Decimal("0")

            booking.save()

            messages.success(
                request,
                "Booking Created Successfully."
            )

            return redirect("booking_list")

    else:

        form = BookingForm()

    return render(
        request,
        "booking/booking_form.html",
        {
            "form": form
        }
    )


# ===============================
# Booking Details
# ===============================
@login_required
def booking_detail(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    return render(
        request,
        "booking/booking_detail.html",
        {
            "booking": booking
        }
    )


# ===============================
# Edit Booking
# ===============================
@login_required
def edit_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    if request.method == "POST":

        form = BookingForm(
            request.POST,
            instance=booking
        )

        if form.is_valid():

            booking = form.save(commit=False)

            distance = request.POST.get("distance", "0")

            try:
                booking.distance = Decimal(distance)
            except:
                booking.distance = Decimal("0")

            if booking.vehicle:

                booking.total_fare = (
                    booking.distance *
                    booking.vehicle.price_per_km
                )

            booking.save()

            messages.success(
                request,
                "Booking Updated Successfully."
            )

            return redirect("booking_list")

    else:

        form = BookingForm(instance=booking)

    return render(
        request,
        "booking/booking_form.html",
        {
            "form": form
        }
    )


# ===============================
# Delete Booking
# ===============================
@login_required
def delete_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    booking.delete()

    messages.success(
        request,
        "Booking Deleted Successfully."
    )

    return redirect("booking_list")
def search_vehicle(request):

    pickup = request.GET.get("pickup")
    drop = request.GET.get("drop")
    date = request.GET.get("date")
    time = request.GET.get("time")

    vehicles = Vehicle.objects.filter(is_available=True)


    context = {
        "pickup": pickup,
        "drop": drop,
        "date": date,
        "time": time,
        "vehicles": vehicles,
    }

    return render(
        request,
        "booking/search_vehicle.html",
        context
    )
