from django.db import models
from vehicle.models import Vehicle
from accounts.models import CustomUser


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

    # Every driver is added by (and works under) a Partner account.
    # The driver may optionally also have their own login (user), so they
    # can log in and manage their own rides directly.
    partner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "PARTNER"},
        related_name="drivers"
    )

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_profile",
        help_text="Optional: link this driver to their own login account."
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

    rc_copy = models.ImageField(
        upload_to="rc/",
        blank=True,
        null=True
    )

    insurance_copy = models.ImageField(
        upload_to="insurance/",
        blank=True,
        null=True
    )

    rating_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00
    )

    total_ratings_count = models.PositiveIntegerField(default=0)

    VERIFICATION_CHOICES = (
        ("PENDING", "Pending Approval"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_CHOICES,
        default="APPROVED"
    )

    rejection_reason = models.CharField(max_length=255, blank=True, default="")

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.rating_score} ★)"