# Generated by Django 4.2.9 on 2024-01-21 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0023_demographics_allergies_demographics_blood_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demographics',
            name='relationship_to_patient',
        ),
        migrations.AddField(
            model_name='demographics',
            name='emergency_contact_relationship_to_patient',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='allergies',
            field=models.CharField(help_text='List the allergies you have if any or type None if none.', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='blood_type',
            field=models.CharField(choices=[('A+', 'A positive'), ('A-', 'A negative'), ('B+', 'B positive'), ('B-', 'B negative'), ('AB+', 'AB positive'), ('AB-', 'AB negative'), ('0+', '0 positive'), ('0-', '0 negative')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='emergency_contact_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='emergency_contact_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='ethnicity',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='preferred_language',
            field=models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ar-dz', 'Algerian Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('ckb', 'Central Kurdish (Sorani)'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('ig', 'Igbo'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kab', 'Kabyle'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('ky', 'Kyrgyz'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('ms', 'Malay'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmål'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('tk', 'Turkmen'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='primary_care_physician_clinic',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='primary_care_physician_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='primary_care_physician_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='race',
            field=models.CharField(max_length=100, null=True),
        ),
    ]