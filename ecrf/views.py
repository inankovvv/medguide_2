from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from accounts.utils import is_verified_doctor

from files.models import File
from files.forms import MultipleFileUploadForm

from .models import Ecrf, Visit, AdverseEvent
from .forms import CreateVisitForm

# Create your views here.


@login_required
def _ecrf(request, trial_id, patient_id):
    """
    This is only a redirect view
    """
    ecrf = get_object_or_404(Ecrf, trial__id=trial_id, patient__id=patient_id)
    return HttpResponseRedirect(reverse("ecrf:ecrf", kwargs={"ecrf_id": ecrf.id}))


@login_required
def ecrf(request, ecrf_id):
    """
    This is the ecrf view
    """
    context = dict()
    ecrf = get_object_or_404(Ecrf, id=ecrf_id)
    context["ecrf"] = ecrf
    return render(request, "ecrf/ecrf.html", context=context)


@login_required
def visit(request, ecrf_id, visit_id):
    context = dict()
    # Check if the ecrf belongs to the user or is created by the doctor

    return render(request, "ecrf/visit.html", context=context)


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def create_visit(request, ecrf_id):
    context = dict()
    ecrf = get_object_or_404(Ecrf, pk=ecrf_id)

    create_visit_form = CreateVisitForm(request.POST or None)
    upload_files_form = MultipleFileUploadForm(
        request.POST or None, request.FILES or None
    )

    ecrf_visits = ecrf.ecrf_visits.exists()  # type: ignore

    if request.method == "POST":
        if create_visit_form.is_valid():

            # First we create the visit
            visit = create_visit_form.save(commit=False)
            visit.ecrf_id = ecrf.id
            if not ecrf_visits:
                visit.pre_study = True
                visit.post_study = False
            visit.save()

            # Then we set the files associated with the visit
            if upload_files_form.is_valid():
                files = upload_files_form.cleaned_data.get("files")
                files_objects = list()
                for f in files:
                    file = File.objects.create(
                        file=f,
                        uploaded_by=request.user,
                    )
                    files_objects.append(file)
                visit.files.set(files_objects)
                # set unlike add fires a signal and saves the object

    context["create_visit_form"] = create_visit_form
    context["upload_files_form"] = upload_files_form
    context["ecrf_visits"] = ecrf_visits

    return render(request, "ecrf/create_visit.html", context=context)
