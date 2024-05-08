from django import forms
from .models import Visit


class CreateVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = [
            "type",
            "post_study",
        ]
