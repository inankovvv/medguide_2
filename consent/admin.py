from django.contrib import admin
from .models import Consent, QRCode, TrialConsent


class ConsentModelAdmin(admin.ModelAdmin):
    readonly_fields = [
        "doctor",
        "patient",
        "date_created",
        "signed",
        "date_signed",
        "date_modified",
        "qr_code",
    ]
    list_filter = [
        "signed",
    ]


class TrialConsentModelAdmin(admin.ModelAdmin):
    def consent_doctor(self, obj):
        return obj.consent.doctor

    def consent_patient(self, obj):
        return obj.consent.patient

    readonly_fields = [
        "consent",
        "consent_doctor",
        "consent_patient",
        "date_created",
        "signed",
        "date_signed",
        "date_modified",
    ]
    list_filter = [
        "signed",
    ]


admin.site.register(Consent, ConsentModelAdmin)
admin.site.register(QRCode)
admin.site.register(TrialConsent, TrialConsentModelAdmin)

# Register your models here.
