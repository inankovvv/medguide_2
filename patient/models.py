import uuid
from django.db import models
from django.conf.global_settings import LANGUAGES
from accounts.models import Doctor
from accounts.models import Patient
from accounts.utils import validate_dob


class PatientProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_user = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="PatientProfile",
        editable=False,
    )

    # If PatientProfile updated yes, verified account for Patient is set - only doctor can verify
    updated = models.BooleanField(default=False)
    first_updated_by = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="first_updated_by",
    )
    last_updated_by = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="last_updated_by",
    )
    first_updated_by_date = models.DateTimeField(blank=True, null=True)
    last_updated_by_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.patient_user}"


class Demographics(models.Model):
    """
    Created simultaneously with PatientProfile
    """

    patient_profile = models.OneToOneField(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="demographics",
        editable=False,
    )

    date_of_birth = models.DateField(
        validators=[
            validate_dob,
        ],
        null=True,
    )

    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
    )

    gender_at_birth = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    preferred_language = models.CharField(max_length=100, choices=LANGUAGES, null=True)
    ethnicity = models.CharField(max_length=100, null=True)
    race = models.CharField(max_length=100, null=True)
    height = models.IntegerField(null=True, help_text="Height in cm")
    weight = models.IntegerField(null=True, help_text="Weight in kg")

    BLOOD_TYPES = (
        ("A+", "A positive"),
        ("A-", "A negative"),
        ("B+", "B positive"),
        ("B-", "B negative"),
        ("AB+", "AB positive"),
        ("AB-", "AB negative"),
        ("0+", "0 positive"),
        ("0-", "0 negative"),
    )

    blood_type = models.CharField(max_length=4, choices=BLOOD_TYPES, null=True)
    allergies = models.CharField(
        max_length=250,
        null=True,
        help_text="List the allergies the patient has if any or type None if none.",
    )

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_phone = models.CharField(max_length=100, null=True)
    emergency_contact_relationship_to_patient = models.CharField(
        max_length=100, null=True
    )

    # Primary Care Physician
    primary_care_physician_name = models.CharField(max_length=100, null=True)
    primary_care_physician_phone = models.CharField(max_length=100, null=True)
    primary_care_physician_clinic = models.CharField(max_length=100, null=True)

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr not in ["_state", "id", "patient_profile_id"]:
                yield attr, value

    def __str__(self):
        return f"{self.patient_profile} Demographics"


class MedicalCondition(models.Model):
    """
    Created only if doctor adds medical condition to PatientProfile
    """

    patient_profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="medical_conditions",
        editable=False,
    )

    # Validate ICD10 Choice - done
    ICD10_code = models.CharField(
        max_length=20,
    )

    disease = models.CharField(max_length=255)
    disease_description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr not in ["_state", "id", "patient_profile_id"]:
                yield attr, value

    def __str__(self):
        return f"{self.ICD10_code} Medical Condition for {self.patient_profile}"


class ConcomitantMedication(models.Model):
    """
    Created only if doctor adds medical condition to PatientProfile and adds conmed to it
    """

    patient_profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="concomitant_medications",
        editable=False,
    )
    medical_condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE)
    drug_inn = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr not in ["_state", "id", "patient_profile_id"]:
                yield attr, value

    def __str__(self):
        return f"{self.drug_inn} {self.patient_profile}"
