# Generated by Django 5.0.1 on 2024-01-10 21:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0004_alter_consent_patient'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='consent',
            name='doctor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='consents_doctor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='consent',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consents_patient', to=settings.AUTH_USER_MODEL),
        ),
    ]