from django.db import models
from booking.models import Booking

class Payment(models.Model):

    PAYMENT_METHOD = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
    )

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    )

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment #{self.id}"