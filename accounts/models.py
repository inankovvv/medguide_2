from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query import QuerySet

from django_countries.fields import CountryField

# Create your models here.


class MGUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MODERATOR = "MODERATOR", "Moderator"
        USER = "USER", "User"
        DOCTOR = "DOCTOR", "MD"
        PATIENT = "PATIENT", "Patient"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    country = models.CharField(
        max_length=200,
        null=True,
        choices=CountryField().choices,
    )

    verified = models.BooleanField(
        default=False,
        help_text="If the user has been verified - Patient by Doctor, Doctor by Admin",
    )

    def get_role_display(self):
        return dict(self.Role.choices)[self.role]

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.get_role_display()} #{self.pk}"


# Doctor Users


class Doctor(MGUser):
    class Meta:
        proxy = True

    objects = BaseUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.Role.DOCTOR
            return super().save(*args, **kwargs)


# Patient Users


class Patient(MGUser):
    class Meta:
        proxy = True

    objects = BaseUserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.Role.PATIENT
            return super().save(*args, **kwargs)
