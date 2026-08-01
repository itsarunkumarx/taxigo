from django import forms
from .models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control finput", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control finput", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control finput", "placeholder": "Email Address"}),
            "phone": forms.TextInput(attrs={"class": "form-control finput", "placeholder": "Phone Number"}),
        }
