from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        exclude = ["total_fare", "created_at"]

        widgets = {
            "customer": forms.Select(attrs={"class":"form-select"}),
            "vehicle": forms.Select(attrs={"class":"form-select"}),
            "driver": forms.Select(attrs={"class":"form-select"}),
            "pickup_location": forms.TextInput(attrs={"class":"form-control"}),
            "drop_location": forms.TextInput(attrs={"class":"form-control"}),
            "booking_date": forms.DateInput(attrs={"type":"date","class":"form-control"}),
            "booking_time": forms.TimeInput(attrs={"type":"time","class":"form-control"}),
            "distance": forms.NumberInput(attrs={"class":"form-control"}),
            "status": forms.Select(attrs={"class":"form-select"}),
        }