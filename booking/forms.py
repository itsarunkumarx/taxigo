from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "booking_category",
            "vehicle_type",
            "payment_method",
        ]

        widgets = {
            "booking_category": forms.Select(attrs={"class": "form-select"}),
            "vehicle_type": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }