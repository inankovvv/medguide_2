import uuid

from django.db import models
from accounts.models import Doctor, Patient
from trial.models import Trial

from files.models import File

# Create your models here.


class Ecrf(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="ecrf_doctor"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, null=True, related_name="ecrf_patient"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    trial = models.ForeignKey(
        Trial, on_delete=models.CASCADE, related_name="trial_ecrfs"
    )

    def __str__(self):
        return f"Ecrf {self.id} for {self.patient} in {self.trial}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "trial"], name="unique_patient_trial_ecrf"
            )
        ]


class Visit(models.Model):
    class VisitType(models.TextChoices):
        F2F = "F2F", "Face to face"
        PHONE = "PHONE", "Phone"

    ecrf = models.ForeignKey(Ecrf, on_delete=models.CASCADE, related_name="ecrf_visits")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=VisitType.choices,
        default=VisitType.F2F,
    )
    pre_study = models.BooleanField(default=False)
    post_study = models.BooleanField(default=False)
    files = models.ManyToManyField(File)

    def __str__(self):
        return f"Patient Visit {self.ecrf.patient} for trial {self.ecrf.trial}"


class AdverseEvent(models.Model):
    ecrf = models.ForeignKey(
        Ecrf, on_delete=models.CASCADE, related_name="ecrf_adverse_events"
    )
    visit = models.ForeignKey(
        Visit, on_delete=models.CASCADE, related_name="visit_adverse_events"
    )
    adverse_event = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return (
            f"Adverse Event for Patient {self.ecrf.patient} for trial {self.ecrf.trial}"
        )
