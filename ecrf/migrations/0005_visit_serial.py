# Generated by Django 5.0.1 on 2024-01-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecrf', '0004_delete_firstvisit_delete_lastvisit'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='serial',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]