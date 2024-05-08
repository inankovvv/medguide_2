import uuid

from django.db import models
from accounts.models import Doctor
from accounts.utils import validate_dob


class MedicalSpecialty(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Medical Specialties"

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_user = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        related_name="DoctorProfile",
        editable=False,
    )

    first_update = models.BooleanField(default=False, editable=False)

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

    medical_specialties = models.ManyToManyField(MedicalSpecialty, related_name="doctor_profiles")
    license_number = models.CharField(max_length=20, null=True)

    YEARS_OF_EXPERIENCE_CHOICES = (
        ("0-5", "0-5 Years"),
        ("6-10", "6-10 Years"),
        ("11-15", "11-15 Years"),
        ("16+", "16+ Years"),
    )

    years_of_experience = models.CharField(
        max_length=5, choices=YEARS_OF_EXPERIENCE_CHOICES, null=True
    )
    phone_number = models.CharField(max_length=15, null=True)
    working_address = models.CharField(max_length=100, null=True, help_text="The address where patients can find you.")
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    postal_code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"Profile: {self.doctor_user}"
