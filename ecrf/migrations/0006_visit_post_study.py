# Generated by Django 5.0.1 on 2024-01-18 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecrf', '0005_visit_serial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='post_study',
            field=models.BooleanField(default=False),
        ),
    ]