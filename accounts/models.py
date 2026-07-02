from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("CUSTOMER", "Customer"),
        ("OWNER", "Car Owner"),
        ("DRIVER", "Driver"),
        ("PARTNER", "Travel Partner"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="CUSTOMER"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username