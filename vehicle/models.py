from django.db import models
from accounts.models import CustomUser


class Vehicle(models.Model):

    VEHICLE_TYPE = (
        ("HATCHBACK", "Hatchback"),
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("LUXURY", "Luxury"),
    )

    FUEL_TYPE = (
        ("PETROL", "Petrol"),
        ("DIESEL", "Diesel"),
        ("CNG", "CNG"),
        ("ELECTRIC", "Electric"),
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "OWNER"}
    )

    vehicle_name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20, unique=True)

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE
    )

    seats = models.PositiveIntegerField()

    price_per_km = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="vehicles/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"