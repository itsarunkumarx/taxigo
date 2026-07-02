from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = "__all__"

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "mobile": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "aadhaar_number": forms.TextInput(attrs={"class": "form-control"}),
            "license_number": forms.TextInput(attrs={"class": "form-control"}),
            "license_expiry": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "experience": forms.NumberInput(attrs={"class": "form-control"}),
            "vehicle": forms.Select(attrs={"class": "form-select"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "license_copy": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "aadhaar_copy": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }