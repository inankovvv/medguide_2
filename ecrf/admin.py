from django.contrib import admin
from django.shortcuts import get_object_or_404
from .models import Ecrf, Visit, AdverseEvent

# Register your models here.

class VisitAdmin(admin.ModelAdmin):
    list_filter = ['type',]

admin.site.register(Ecrf)
admin.site.register(Visit, VisitAdmin)
admin.site.register(AdverseEvent)

