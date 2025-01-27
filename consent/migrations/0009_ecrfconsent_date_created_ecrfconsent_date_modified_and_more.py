# Generated by Django 5.0.1 on 2024-01-10 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consent', '0008_ecrfconsent_signed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecrfconsent',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 10, 23, 28, 48, 507173, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ecrfconsent',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ecrfconsent',
            name='date_signed',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
