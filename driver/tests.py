from django.test import TestCase
from accounts.models import CustomUser
from driver.models import Driver

class DriverProfileTests(TestCase):
    def setUp(self):
        self.partner = CustomUser.objects.create_user(
            username="partner_user",
            password="Password123!",
            role="PARTNER"
        )
        self.driver_user = CustomUser.objects.create_user(
            username="driver_user",
            password="Password123!",
            role="DRIVER"
        )

    def test_create_driver_profile(self):
        """Test creating driver profile linked to partner."""
        driver = Driver.objects.create(
            partner=self.partner,
            user=self.driver_user,
            full_name="Arun Kumar",
            gender="Male",
            dob="1998-05-15",
            experience=3,
            mobile="9876543210",
            license_number="TN202612345",
            license_expiry="2030-12-31",
            verification_status="APPROVED"
        )
        self.assertEqual(driver.full_name, "Arun Kumar")
        self.assertEqual(driver.verification_status, "APPROVED")
        self.assertIn("Arun Kumar", str(driver))
