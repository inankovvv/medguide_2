import os
import uuid
from django.db import models
from django.core.validators import FileExtensionValidator
from django.conf import settings
from .s3_utils import get_s3_object_url as get_s3
from accounts.models import MGUser
from django.utils import timezone

# Create your models here.


def user_directory_path(instance, filename):
    timestamp = timezone.now()
    return f"medical_data/{instance.uploaded_by}/{instance.uploaded_by}-{timestamp}-{filename}"


def qr_code_directory_path(instance, filename):
    return f"consents/{filename}"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(MGUser, on_delete=models.SET_NULL, null=True)
    file = models.FileField(
        upload_to=user_directory_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "png",
                    "jpg",
                    "jpeg",
                    "gif",
                ]
            )
        ],
    )
    name = models.CharField(max_length=255, editable=False)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = self.file.file.name
        if not self.description:
            self.description = self.file.file.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.name}"

    def get_file_s3_url(self):
        s3_object_url = get_s3(
            settings.AWS_STORAGE_BUCKET_NAME, file_key=self.file.file.name
        )
        return s3_object_url
