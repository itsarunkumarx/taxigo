from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Driver
from .forms import DriverForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from booking.models import Booking
@login_required
def driver_dashboard(request):
    return render(request, "driver/dashboard.html")


def driver_list(request):

    search = request.GET.get("search")

    drivers = Driver.objects.all()

    if search:
        drivers = drivers.filter(
            Q(full_name__icontains=search) |
            Q(mobile__icontains=search) |
            Q(license_number__icontains=search)
        )

    paginator = Paginator(drivers, 5)   # 5 drivers per page

    page = request.GET.get("page")

    drivers = paginator.get_page(page)

    context = {
        "drivers": drivers,
        "search": search,
    }

    return render(request, "driver/driver_list.html", context)

def add_driver(request):

    if request.method == "POST":

        form = DriverForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("driver_list")

    else:
        form = DriverForm()

    return render(
        request,
        "driver/driver_form.html",
        {"form": form}
    )

def edit_driver(request, id):

    driver = get_object_or_404(Driver, id=id)

    if request.method == "POST":

        form = DriverForm(
            request.POST,
            request.FILES,
            instance=driver
        )

        if form.is_valid():
            form.save()
            return redirect("driver_list")

    else:
        form = DriverForm(instance=driver)

    return render(
        request,
        "driver/driver_form.html",
        {"form": form}
    )

def delete_driver(request, id):

    driver = get_object_or_404(Driver, id=id)

    if request.method == "POST":
        driver.delete()
        return redirect("driver_list")

    return render(
        request,
        "driver/driver_delete.html",
        {"driver": driver}
    )

def driver_rides(request):

    driver = request.user.driver_profile

    bookings = Booking.objects.filter(driver=driver)

    return render(
        request,
        "driver/driver_rides.html",
        {"bookings": bookings},
    )


def accept_ride(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = "Accepted"
    booking.save()

    return redirect("driver_rides")


def start_ride(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = "On Ride"
    booking.save()

    return redirect("driver_rides")


def complete_ride(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    booking.status = "Completed"
    booking.save()

    booking.vehicle.is_available = True
    booking.vehicle.save()

    booking.driver.status = "Available"
    booking.driver.save()

    return redirect("driver_rides")