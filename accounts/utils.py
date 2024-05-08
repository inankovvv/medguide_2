from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Doctor, Patient

# from django.urls import reverse_lazy


def is_verified_doctor(user):
    has_group = user.groups.filter(name="Doctors").exists()
    return (
        user.is_authenticated
        and (user.role == user.Role.DOCTOR)
        and user.verified
        and has_group
    )


def is_verified_patient(user):
    has_group = user.groups.filter(name="Patients").exists()
    return (
        user.is_authenticated
        and (user.role == user.Role.PATIENT)
        and user.verified
        and has_group
    )


def is_not_verified_doctor(user):
    has_group = user.groups.filter(name="Doctors").exists()
    return user.is_authenticated and (user.role == user.Role.DOCTOR) and has_group


def is_not_verified_patient(user):
    has_group = user.groups.filter(name="Patients").exists()
    return user.is_authenticated and (user.role == user.Role.PATIENT) and has_group


# @user_passes_test(is_verified_doctor, login_url=reverse_lazy('profile')


def validate_dob(value):
    """
    For profile data of birth
    Validate date of birth - user is at least 12 years old and not born in the future
    """
    today = timezone.now().date()
    min_date = today - timezone.timedelta(days=12 * 365)
    if value > today:
        raise ValidationError("Date of birth cannot be in the future")
    elif value > min_date:
        raise ValidationError(
            "You must be at least 12 years old to create a patient profile"
        )
