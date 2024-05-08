from django import forms
from allauth.account.forms import SignupForm
from allauth.utils import generate_unique_username
from django_countries.data import COUNTRIES
from .models import Patient, Doctor


class AccountSignupForm(SignupForm):
    USER_CHOICES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
    )

    countries = [("", "Select Country")]
    countries += [(key, val) for key, val in COUNTRIES.items()]
    country = forms.ChoiceField(choices=countries)
    account_type = forms.ChoiceField(label="I am a", choices=USER_CHOICES, widget=forms.Select)
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")

    def save(self, request):
        account_type = self.cleaned_data.get("account_type")

        if account_type == "patient":
            user = Patient()
        elif account_type == "doctor":
            user = Doctor()
        else:
            raise ValueError("Invalid user type")

        user.username = generate_unique_username(
            txts=[
                self.cleaned_data.get("email"),
            ]
        )
        user.email = self.cleaned_data.get("email")
        user.country = self.cleaned_data.get("country")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.set_password(self.cleaned_data.get("password1"))
        user.save()

        return user
