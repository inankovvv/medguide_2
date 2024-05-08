from django.contrib import admin
from .models import MGUser, Doctor, Patient

# Register your models here.

class MGUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'role', 'verified', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role', 'verified', 'country']

admin.site.register(MGUser, MGUserAdmin)
