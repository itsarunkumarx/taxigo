from django.db import models
from accounts.models import CustomUser


class Vehicle(models.Model):

    VEHICLE_TYPE = (
        ("AUTO", "Auto / Rickshaw"),
        ("MINI", "Mini"),
        ("HATCHBACK", "Hatchback"),
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("LUXURY", "Luxury"),
        ("PREMIUM", "Premium"),
    )

    FUEL_TYPE = (
        ("PETROL", "Petrol"),
        ("DIESEL", "Diesel"),
        ("CNG", "CNG"),
        ("ELECTRIC", "Electric"),
    )

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehicles"
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

    # Driver Details (Configured by Admin)
    driver_name = models.CharField(max_length=100, blank=True, default="Ramesh Kumar")
    driver_phone = models.CharField(max_length=20, blank=True, default="+91 98452 98351")
    driver_image = models.ImageField(upload_to="drivers/", blank=True, null=True)
    driver_rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.9)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        if self.image:
            try:
                return self.image.url
            except Exception:
                pass
        fallback_map = {
            "LUXURY": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=600&auto=format&fit=crop&q=80",
            "SUV": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600&auto=format&fit=crop&q=80",
            "SEDAN": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600&auto=format&fit=crop&q=80",
            "HATCHBACK": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600&auto=format&fit=crop&q=80",
            "MINI": "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=600&auto=format&fit=crop&q=80",
        }
        return fallback_map.get(self.vehicle_type, "https://images.unsplash.com/photo-1596484552834-6a58f850e0a1?w=600&auto=format&fit=crop&q=80")

    def get_driver_image_url(self):
        if self.driver_image:
            try:
                return self.driver_image.url
            except Exception:
                pass
        fallback_map = {
            "LUXURY": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            "SUV": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        }
        return fallback_map.get(self.vehicle_type, "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80")

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"