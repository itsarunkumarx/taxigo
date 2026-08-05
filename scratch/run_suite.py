import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rovexa.settings")
django.setup()

from booking.tests import PricingEngineTests, BookingFormValidationTests
from accounts.tests import UserAccountTests
from driver.tests import DriverProfileTests
from vehicle.tests import VehicleModelTests
from payment.tests import WalletLedgerTests

def run_all():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PricingEngineTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(BookingFormValidationTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(UserAccountTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(DriverProfileTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(VehicleModelTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WalletLedgerTests))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n==================================================")
    print(f"RESULTS: {result.testsRun} Tests Executed | Failures: {len(result.failures)} | Errors: {len(result.errors)}")
    print("==================================================")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
