import uuid
from django.db import models

# Create your models here.

class Trial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indication = models.CharField(max_length=255)
    drug = models.CharField(max_length=255)
    # TODO : Add inclusion and exclusion criteria, Start and End date

    def __str__(self):
        return f"Trial {self.id}, {self.indication}"
