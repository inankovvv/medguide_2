# Generated by Django 5.0.1 on 2024-01-10 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_doctor_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mguser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('MODERATOR', 'Moderator'), ('USER', 'User'), ('DOCTOR', 'Medical Doctor'), ('PATIENT', 'Patient')], default='USER', max_length=20),
        ),
    ]
