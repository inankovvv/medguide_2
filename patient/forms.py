from django import forms
from django.shortcuts import get_object_or_404
from .models import (
    PatientProfile,
    Demographics,
    MedicalCondition,
    ConcomitantMedication,
)


class UpdatePatientDemographicsForm(forms.ModelForm):
    class Meta:
        model = Demographics
        exclude = [
            "id",
            "patient_user",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class MedicalConditionForm(forms.ModelForm):
    class Meta:
        model = MedicalCondition
        fields = ["ICD10_code", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class ConcomitantMedicationForm(forms.ModelForm):
    class Meta:
        model = ConcomitantMedication
        fields = ["drug_inn", "medical_condition", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        patient_profile = kwargs.pop("patient_profile", None)
        super(ConcomitantMedicationForm, self).__init__(*args, **kwargs)

        if isinstance(patient_profile, PatientProfile):
            medical_conditions = MedicalCondition.objects.filter(
                patient_profile=patient_profile
            )
            self.fields["medical_condition"].queryset = medical_conditions
