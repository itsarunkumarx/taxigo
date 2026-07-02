from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "driver",
        "vehicle",
        "booking_date",
        "status",
        "total_fare",
    )

    list_filter = (
        "status",
        "booking_date",
    )

    search_fields = (
        "customer__username",
        "pickup_location",
        "drop_location",
    )