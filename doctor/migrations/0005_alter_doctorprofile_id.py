# Generated by Django 5.0.1 on 2024-01-14 15:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0004_alter_doctorprofile_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]