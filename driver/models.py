from django.db import models
from vehicle.models import Vehicle
from accounts.models import CustomUser
user = models.OneToOneField(
    CustomUser,
    on_delete=models.CASCADE,
    limit_choices_to={"role": "DRIVER"},
    related_name="driver_profile"
)

class Driver(models.Model):

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    STATUS = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER)
    dob = models.DateField()

    mobile = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    aadhaar_number = models.CharField(max_length=12)

    license_number = models.CharField(max_length=30)

    license_expiry = models.DateField()

    experience = models.PositiveIntegerField()

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to="drivers/",
        blank=True,
        null=True
    )

    license_copy = models.ImageField(
        upload_to="licenses/",
        blank=True,
        null=True
    )

    aadhaar_copy = models.ImageField(
        upload_to="aadhaar/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name