from django import forms

from doctor.models import DoctorProfile

class UpdateDoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        exclude = ["id", "doctor_user", "first_update", ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
