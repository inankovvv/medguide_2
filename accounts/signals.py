from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Doctor, Patient
from doctor.models import DoctorProfile
from patient.models import PatientProfile


@receiver(post_save, sender=Patient)
def add_patient_profile_and_group(sender, instance, **kwargs):
    if kwargs.get("created", False):
        patients_group, created = Group.objects.get_or_create(name="Patients")
        instance.groups.add(patients_group)

        patient_profile, created = PatientProfile.objects.get_or_create(
            patient_user=instance
        )


@receiver(post_save, sender=Doctor)
def add_doctor_profile_and_group(sender, instance, **kwargs):
    if kwargs.get("created", False):
        doctors_group, created = Group.objects.get_or_create(name="Doctors")
        instance.groups.add(doctors_group)

        doctor_profile, created = DoctorProfile.objects.get_or_create(
            doctor_user=instance
        )
