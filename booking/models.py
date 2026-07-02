from django.db import models
from accounts.models import CustomUser
from vehicle.models import Vehicle
from driver.models import Driver
from decimal import Decimal

class Booking(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("On Ride", "On Ride"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customer_bookings"
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    pickup_location = models.CharField(max_length=255)

    drop_location = models.CharField(max_length=255)

    booking_date = models.DateField()

    booking_time = models.TimeField()

    distance = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    total_fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id}"