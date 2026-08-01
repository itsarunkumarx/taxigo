from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from accounts.decorators import role_required
from .models import Vehicle
from .forms import VehicleForm


def _vehicles_queryset(request):
    """Admins see every vehicle. Partners only see their own."""
    if request.user.role == "ADMIN":
        return Vehicle.objects.all()
    return Vehicle.objects.filter(owner=request.user)


def _build_form(request, *args, **kwargs):
    """
    Build a VehicleForm and, for Partners, remove the 'owner' field
    entirely (it's set automatically to request.user in the view) so
    that it is neither required nor rendered for them.
    """
    form = VehicleForm(*args, **kwargs)
    if request.user.role == "PARTNER":
        form.fields.pop("owner", None)
    return form


@role_required("ADMIN", "PARTNER")
def vehicle_list(request):

    search = request.GET.get("search") or ""

    vehicles = _vehicles_queryset(request)

    if search:
        vehicles = vehicles.filter(
            Q(vehicle_name__icontains=search) |
            Q(vehicle_number__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search)
        )

    paginator = Paginator(vehicles, 5)
    page = request.GET.get("page")
    vehicles = paginator.get_page(page)

    context = {
        "vehicles": vehicles,
        "search": search,
    }

    return render(request, "vehicle/vehicle_list.html", context)


@role_required("ADMIN", "PARTNER")
def add_vehicle(request):

    if request.method == "POST":

        form = _build_form(request, request.POST, request.FILES)

        if form.is_valid():
            vehicle = form.save(commit=False)
            if request.user.role == "PARTNER":
                vehicle.owner = request.user
            vehicle.save()
            messages.success(request, "Vehicle added successfully.")
            return redirect("vehicle_list")

    else:
        form = _build_form(request)

    return render(request, "vehicle/vehicle_form.html", {"form": form})


@role_required("ADMIN", "PARTNER")
def edit_vehicle(request, id):

    vehicle = get_object_or_404(_vehicles_queryset(request), id=id)

    if request.method == "POST":

        form = _build_form(request, request.POST, request.FILES, instance=vehicle)

        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect("vehicle_list")

    else:
        form = _build_form(request, instance=vehicle)

    return render(request, "vehicle/vehicle_form.html", {"form": form})


@role_required("ADMIN", "PARTNER")
def delete_vehicle(request, id):

    vehicle = get_object_or_404(_vehicles_queryset(request), id=id)

    if request.method == "POST":
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully.")
        return redirect("vehicle_list")

    return render(request, "vehicle/vehicle_delete.html", {"vehicle": vehicle})
