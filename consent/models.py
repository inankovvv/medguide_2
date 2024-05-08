import uuid
from django.db import models
from django.conf import settings
from accounts.models import MGUser
from trial.models import Trial
from ecrf.models import Ecrf
from files.models import qr_code_directory_path

# Create your models here.


class Consent(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    doctor = models.ForeignKey(
        MGUser, on_delete=models.CASCADE, related_name="ConsentsDoctor", editable=False
    )
    patient = models.ForeignKey(
        MGUser,
        on_delete=models.CASCADE,
        related_name="ConsentsPatient",
        blank=True,
        null=True,
        editable=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False, editable=False)
    date_signed = models.DateTimeField(blank=True, null=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    qr_code = models.OneToOneField(
        "QRCode", on_delete=models.CASCADE, related_name="ConsentQRCode", editable=False
    )

    def __str__(self):
        return f"Consent - {self.id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "patient"], name="consent_constraint_doctor_patient"
            )
        ]


class QRCode(models.Model):
    consent = models.ForeignKey(
        Consent,
        on_delete=models.CASCADE,
        editable=False,
        related_name="TrialQRCodes",
        null=True,
    )
    secret = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code = models.ImageField(
        upload_to=qr_code_directory_path, editable=False, null=True
    )

    def save(self, commit_qr=True, *args, **kwargs):
        if commit_qr:
            from qrcode import make
            from io import BytesIO
            from django.core.files import File
            from django.urls import reverse

            path_to_consent = settings.BASE_URL + reverse(
                "consent:accept_consent",
                kwargs={
                    "consent_id": self.consent.id,  # type: ignore
                },
            )
            data = str(path_to_consent)  # type: ignore
            img = make(data)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.qr_code.save(
                f"qr_code_{self.secret}.png", File(buffer), save=False
            )
        super(QRCode, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"QRCode {self.pk} - {str(self.secret)}"

    def get_qr_s3_url(self):
        from files.s3_utils import get_s3_object_url as get_s3
        s3_object_url = get_s3(settings.AWS_STORAGE_BUCKET_NAME, file_key=self.qr_code.file.name)
        return s3_object_url


class TrialConsent(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    consent = models.ForeignKey(
        Consent, on_delete=models.CASCADE, editable=False, related_name="TrialConsents"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    signed = models.BooleanField(default=False)
    date_signed = models.DateTimeField(blank=True, null=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    trial = models.ForeignKey(
        Trial, on_delete=models.CASCADE, related_name="TrialTrialConsents"
    )

    def __str__(self):
        return f"Trial Consent - {self.id}"
