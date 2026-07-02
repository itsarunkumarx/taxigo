from django.shortcuts import render, redirect
from .models import Vehicle
from .forms import VehicleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
def vehicle_list(request):

    vehicles = Vehicle.objects.all()

    return render(
        request,
        "vehicle/vehicle_list.html",
        {"vehicles": vehicles}
    )


def add_vehicle(request):

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("vehicle_list")

    else:

        form = VehicleForm()

    return render(
        request,
        "vehicle/vehicle_form.html",
        {"form": form}
    )
def edit_vehicle(request, id):

    vehicle = Vehicle.objects.get(id=id)

    if request.method == "POST":

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle
        )

        if form.is_valid():
            form.save()
            return redirect("vehicle_list")

    else:

        form = VehicleForm(instance=vehicle)

    return render(
        request,
        "vehicle/vehicle_form.html",
        {"form": form}
    )



def delete_vehicle(request, id):

    vehicle = get_object_or_404(Vehicle, id=id)

    if request.method == "POST":
        vehicle.delete()
        return redirect("vehicle_list")

    return render(
        request,
        "vehicle/vehicle_delete.html",
        {"vehicle": vehicle}
    )

def vehicle_list(request):

    search = request.GET.get("search")

    vehicles = Vehicle.objects.all()

    if search:

        vehicles = vehicles.filter(
            Q(vehicle_name__icontains=search) |
            Q(vehicle_number__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search)
        )

    context = {
        "vehicles": vehicles,
        "search": search,
    }

    return render(request, "vehicle/vehicle_list.html", context)

def vehicle_list(request):

    search = request.GET.get("search")

    vehicles = Vehicle.objects.all()

    if search:
        vehicles = vehicles.filter(
            Q(vehicle_name__icontains=search) |
            Q(vehicle_number__icontains=search) |
            Q(brand__icontains=search)
        )

    paginator = Paginator(vehicles, 5)

    page = request.GET.get("page")

    vehicles = paginator.get_page(page)

    context = {
        "vehicles": vehicles,
        "search": search,
    }

    return render(request, "vehicle/vehicle_list.html", context)