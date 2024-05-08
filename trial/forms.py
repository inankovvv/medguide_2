from django import forms
from consent.models import Consent


class PatientModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return (
            f"{obj.patient.last_name}, {obj.patient.first_name}, {obj.patient.email}"  # type: ignore
            if obj.patient  # type: ignore
            else "No Patient Assigned"
        )


class EnrollPatientForm(forms.Form):
    patient = PatientModelChoiceField(queryset=Consent.objects.none())

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop("doctor", None)
        consented_patients = Consent.objects.filter(doctor=doctor, signed=True)
        super().__init__(*args, **kwargs)

        if doctor:
            self.fields["patient"].queryset = consented_patients.all()
