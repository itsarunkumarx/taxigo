from django import forms
from .models import Vehicle

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle
        fields = "__all__"

        widgets = {
            "owner": forms.Select(attrs={"class":"form-select"}),
            "vehicle_name": forms.TextInput(attrs={"class":"form-control"}),
            "brand": forms.TextInput(attrs={"class":"form-control"}),
            "model": forms.TextInput(attrs={"class":"form-control"}),
            "vehicle_number": forms.TextInput(attrs={"class":"form-control"}),
            "vehicle_type": forms.Select(attrs={"class":"form-select"}),
            "fuel_type": forms.Select(attrs={"class":"form-select"}),
            "seats": forms.NumberInput(attrs={"class":"form-control"}),
            "price_per_km": forms.NumberInput(attrs={"class":"form-control"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }