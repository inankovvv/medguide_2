from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from accounts.utils import is_verified_doctor
from consent.models import TrialConsent
from .models import Trial
from .forms import EnrollPatientForm

# Create your views here.


@login_required
@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def trial(request, trial_id):
    context = dict()

    trial = get_object_or_404(Trial, id=trial_id)
    enroll_patient_form = EnrollPatientForm(request.POST or None, doctor=request.user)

    if request.method == "POST":
        if enroll_patient_form.is_valid():
            patient = enroll_patient_form.cleaned_data.get("patient")
            return HttpResponseRedirect(
                reverse(
                    "consent:create_trial_consent",
                    kwargs={"trial_id": trial_id, "patient_id": patient.patient.id},
                )
            )

    context["trial"] = trial
    context["enroll_patient_form"] = enroll_patient_form

    return render(request, "trial/trial.html", context=context)


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def view_all_trials(request):
    context = dict()
    trials = Trial.objects.all()
    context["trials"] = trials
    return render(request, "trial/view_all_trials.html", context=context)


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def enrolled_patients(request):
    context = dict()
    trial_consents = TrialConsent.objects.filter(consent__doctor=request.user)
    context["trial_consents"] = trial_consents

    return render(request, "trial/enrolled_patients.html", context=context)

