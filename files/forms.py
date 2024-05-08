from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from .models import File


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleFileUploadForm(forms.Form):
    files = MultipleFileField()  # type: ignore

    def clean_files(self):
        files = self.cleaned_data["files"]
        allowed_extensions = ["pdf", "doc", "docx", "png", "jpg", "jpeg", "gif"]
        validator = FileExtensionValidator(allowed_extensions=allowed_extensions)

        for file in files:
            try:
                validator(file)
            except ValidationError as e:
                raise forms.ValidationError(
                    f"File {file.name} has an invalid extension."
                )

        return files


class SingleFileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file", "description"]
