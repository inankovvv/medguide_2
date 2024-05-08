from django.contrib import admin
from .models import DoctorProfile, MedicalSpecialty
# Register your models here.

class DoctorProfileModelAdmin(admin.ModelAdmin):
    readonly_fields = ['doctor_user',]

admin.site.register(DoctorProfile, DoctorProfileModelAdmin)
admin.site.register(MedicalSpecialty)