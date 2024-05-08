from django.utils import timezone
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import Doctor, Patient
from accounts.utils import (
    is_verified_doctor,
    is_verified_patient,
    is_not_verified_patient,
)
from .models import Consent, QRCode, TrialConsent
from trial.models import Trial
from ecrf.models import Ecrf

# Create your views here.


# CREATE CONSENT
@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def create_consent(request):
    context = dict()
    unsigned_consents = Consent.objects.filter(
        doctor=request.user, signed=False
    ).count()
    if unsigned_consents < 2:
        if request.method == "POST":
            qr_code = QRCode()
            qr_code.save(commit_qr=False)
            consent = Consent()
            consent.doctor = request.user
            consent.qr_code = qr_code
            consent.save()
            qr_code.consent = consent
            qr_code.save()
            return HttpResponseRedirect(
                reverse("consent:view_consent", kwargs={"consent_id": consent.id})
            )
    else:
        messages.info(
            request,
            "You already have 2 unsigned consents. Please make sure a patient signs at least 1 of them.",
        )
    return render(request, "consent/create_consent.html", context=context)


# ACCEPT CONSENT
@user_passes_test(is_not_verified_patient, login_url="accounts:user_profile")
def accept_consent(request, consent_id):
    context = dict()
    consent = get_object_or_404(Consent, id=consent_id)
    qr_code = get_object_or_404(QRCode, secret=consent.qr_code.secret)
    if request.method == "POST":
        if not consent.signed:
            patient = request.user
            if not patient.verified:
                patient.verified = True
                patient.save()
            consent.patient = patient
            consent.signed = True
            consent.date_signed = timezone.now()
            consent.save()
    context["consent"] = consent
    return render(request, "consent/accept_consent.html", context=context)


# VIEW CONSENT
@login_required
def view_consent(request, consent_id):
    context = dict()
    if is_verified_doctor(request.user):
        consent = get_object_or_404(Consent, id=consent_id, doctor=request.user)
    else:
        consent = get_object_or_404(Consent, id=consent_id, patient=request.user)

    qr_code_url = consent.qr_code.get_qr_s3_url()
    context["consent"] = consent
    context["qr_code_url"] = qr_code_url
    return render(request, "consent/view_consent.html", context=context)


# VIEW ALL CONSENTS
@login_required
def view_all_consents(request):
    context = dict()
    user = request.user
    consents = None
    if is_verified_doctor(user):
        consents = Consent.objects.filter(doctor=user)
    elif is_verified_patient(user):
        consents = Consent.objects.filter(patient=user)
    elif request.user.is_staff:
        consents = Consent.objects.all()
    context["consents"] = consents  # type: ignore
    return render(request, "consent/view_all_consents.html", context=context)


# VIEW CONSENTED PATIENTS - CONSENTED PATIENTS BY DOCTOR
@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def view_consented_patients(request):
    context = dict()
    consented_patients = Consent.objects.filter(doctor=request.user, signed=True)

    context["consented_patients"] = consented_patients

    return render(request, "consent/view_consented_patients.html", context=context)


# CREATE TRIAL CONSENT
@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def create_trial_consent(request, trial_id, patient_id):
    context = dict()
    patient = get_object_or_404(Patient, pk=patient_id)
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient, signed=True
    )
    trial = get_object_or_404(Trial, pk=trial_id)

    # Check if there is already a trial consent for this patient
    is_trial_consent = TrialConsent.objects.filter(
        trial=trial, consent__patient=patient
    )
    patient_profile_updated = patient.PatientProfile.updated  # type: ignore
    if not is_trial_consent.exists() and patient_profile_updated:
        if request.method == "POST":
            trial_consent = TrialConsent()
            trial_consent.consent = consent
            trial_consent.trial = trial
            trial_consent.save()
            messages.success(
                request,
                "Trial Consent has been submitted. Please, notify your patient to sign it.",
            )
    else:
        if not patient_profile_updated:
            messages.error(
                request,
                "Patient Profile has not been updated. Please update the patient profile, so that you can submit a trial consent.",
            )
        else:
            if is_trial_consent.get().signed:
                messages.error(
                    request, "Trial Consent has already been created and signed."
                )
            else:
                messages.error(
                    request,
                    "Trial Consent has already been created, but not yet signed. Remind your patient.",
                )

    context["patient"] = patient
    context["consent"] = consent
    return render(request, "consent/create_trial_consent.html", context=context)


# ACCEPT TRIAL CONSENT
@user_passes_test(is_verified_patient, login_url="accounts:profile")
def accept_trial_consent(request, trial_consent_id):
    """
    In create_trial_consent we have already checked that there is such a patient and consent. Without them a trial_consent wouldn't
    be created, so accepting it is ok.
    """
    context = dict()
    trial_consent = get_object_or_404(TrialConsent, id=trial_consent_id)
    if request.method == "POST":
        if trial_consent.consent.patient == request.user and not trial_consent.signed:
            trial_consent.signed = True
            trial_consent.date_signed = timezone.now()
            trial_consent.save()
            ecrf = Ecrf(
                doctor=trial_consent.consent.doctor,
                patient=trial_consent.consent.patient,
                trial=trial_consent.trial,
            )
            ecrf.save()

    context["trial_consent"] = trial_consent
    return render(request, "consent/accept_trial_consent.html", context=context)
