from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from accounts.utils import is_verified_doctor

from .models import File
from .forms import MultipleFileUploadForm, SingleFileUploadForm

# Create your views here.


@staff_member_required
def view_file(request, file_id):
    context = dict()
    file = get_object_or_404(File, id=file_id)
    file_url = file.get_file_s3_url()
    context["file"] = file
    context["file_url"] = file_url
    return render(request, "files/view_file.html", context=context)


@staff_member_required
def upload_file(request):
    context = dict()
    file_upload_form = SingleFileUploadForm(request.POST or None, request.FILES or None)
    if file_upload_form.is_valid():
        file = file_upload_form.save(commit=False)
        file.uploaded_by = request.user
        file.save()

    context["file_upload_form"] = file_upload_form
    return render(request, "files/upload_file.html", context=context)


@staff_member_required
def upload_multiple_files(request):
    context = dict()
    multiple_file_upload_form = MultipleFileUploadForm(
        request.POST or None, request.FILES or None
    )
    if multiple_file_upload_form.is_valid():
        files = multiple_file_upload_form.cleaned_data.get("files")
        for f in files:
            file = File.objects.create(
                file=f,
                uploaded_by=request.user,
            )

    context["file_upload_form"] = multiple_file_upload_form
    return render(request, "files/upload_file.html", context=context)
