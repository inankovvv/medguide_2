from django.contrib import admin
from .models import PatientProfile, Demographics, MedicalCondition, ConcomitantMedication

# Register your models here.
class DemographicsModelAdmin(admin.ModelAdmin):
    readonly_fields = ['patient_profile',]

class MedicalConditionModelAdmin(admin.ModelAdmin):
    readonly_fields = ['patient_profile',]

class ConcomitantMedicationModelAdmin(admin.ModelAdmin):
    readonly_fields = ['patient_profile',]

class PatientProfileModelAdmin(admin.ModelAdmin):
    readonly_fields = ['patient_user',]

admin.site.register(PatientProfile, PatientProfileModelAdmin)
admin.site.register(Demographics, DemographicsModelAdmin)
admin.site.register(MedicalCondition, MedicalConditionModelAdmin)
admin.site.register(ConcomitantMedication, ConcomitantMedicationModelAdmin)

