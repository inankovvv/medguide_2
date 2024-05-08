from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import PatientProfile, Demographics

@receiver(post_save, sender=PatientProfile)
def add_patient_data_to_profile(sender, instance, **kwargs):
    if kwargs.get("created", False):
        demographics, created = Demographics.objects.get_or_create(patient_profile=instance)
