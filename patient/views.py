import icd10

from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.utils import timezone

from accounts.utils import is_verified_doctor, is_verified_patient
from consent.models import Consent

from .models import (
    PatientProfile,
    Demographics,
    MedicalCondition,
    ConcomitantMedication,
)
from .forms import (
    UpdatePatientDemographicsForm,
    MedicalConditionForm,
    ConcomitantMedicationForm,
)

# Create your views here.
# NB! Profile_ID is the id of the PatientProfile, not the MGUser ID - Extra Layer of security


@login_required
def patient_profile(request, profile_id=None):
    """
    Is sent to accounts user_profile view
    """
    context = dict()
    if profile_id and is_verified_doctor(request.user):
        # Check if doctor and patient have consent before doctor views patient profile
        patient_profile = get_object_or_404(PatientProfile, id=profile_id)
        consent = get_object_or_404(Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True)
    elif is_verified_patient(request.user):
        profile_pk = request.user.PatientProfile.pk
        patient_profile = get_object_or_404(PatientProfile, pk=profile_pk)
    else:
        patient_profile = None

    context["patient_profile"] = patient_profile

    return render(request, "patient/patient_profile.html", context=context)


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def update_patient_profile(request, profile_id):
    """
    Update PatientProfile and Demographics
    """
    context = dict()
    patient_profile = get_object_or_404(PatientProfile, pk=profile_id)

    # Check if there is consent between the doctor and patient
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True
    )

    # Forms in PatientProfile
    demographics_form = UpdatePatientDemographicsForm(request.POST or None, instance=patient_profile.demographics)  # type: ignore
    medical_condition_form = MedicalConditionForm()
    concomitant_medication_form = ConcomitantMedicationForm(
        patient_profile=patient_profile
    )

    # Queries for Conditions and Medications
    medical_conditions = MedicalCondition.objects.filter(
        patient_profile=patient_profile
    ).all()

    concomitant_medications = ConcomitantMedication.objects.filter(
        patient_profile=patient_profile
    ).all()

    if request.method == "POST":
        if demographics_form.is_valid():
            if not patient_profile.updated:
                patient_profile.updated = True
                patient_profile.first_updated_by = request.user
                patient_profile.first_updated_by_date = timezone.now()
            patient_profile.last_updated_by = request.user
            patient_profile.last_updated_by_date = timezone.now()
            patient_profile.save()
            demographics_form.save()

    context["patient_profile"] = patient_profile
    context["demographics_form"] = demographics_form
    context["medical_condition_form"] = medical_condition_form
    context["medical_conditions"] = medical_conditions
    context["concomitant_medication_form"] = concomitant_medication_form
    context["concomitant_medications"] = concomitant_medications

    return render(request, "patient/update_patient_profile.html", context=context)


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def update_medical_condition(request, profile_id):
    """
    Add and Update Medical Conditions
    """
    patient_profile = get_object_or_404(PatientProfile, pk=profile_id)
    medical_condition_form = MedicalConditionForm(request.POST or None)
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True
    )
    if request.method == "POST":
        if medical_condition_form.is_valid():
            medical_condition = medical_condition_form.save(commit=False)
            icd10_code = medical_condition_form.cleaned_data.get("ICD10_code").upper() # type: ignore
            condition_for_patient_exists = MedicalCondition.objects.filter(
                patient_profile=patient_profile, ICD10_code=icd10_code
            )
            if not condition_for_patient_exists:
                if icd10.exists(icd10_code):
                    icd10_code = icd10.find(icd10_code)
                    medical_condition.ICD10_code = icd10_code
                    medical_condition.disease = f"{icd10_code.description}"  # type: ignore
                    medical_condition.disease_description = f"{icd10_code.block_description}"  # type: ignore
                    medical_condition.patient_profile = patient_profile
                    medical_condition.save()
                    messages.success(
                        request,
                        "Medical Condition has been added, please update concomitant medication",
                    )
                else:
                    messages.error(
                        request,
                        "Please, check the ICD10 code again and input as per global ICD10 guidelines.",
                    )
            else:
                messages.error(
                    request, "This condition is already registered for this Patient."
                )

    return HttpResponseRedirect(
        reverse("patient:update_patient_profile", kwargs={"profile_id": profile_id})
    )


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def delete_medical_condition(request, profile_id, condition_id):
    patient_profile = get_object_or_404(PatientProfile, pk=profile_id)
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True
    )
    medical_condition = get_object_or_404(MedicalCondition, pk=condition_id)
    medical_condition.delete()

    return HttpResponseRedirect(
        reverse("patient:update_patient_profile", kwargs={"profile_id": profile_id})
    )


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def update_concomitant_medication(request, profile_id):
    """
    Add and Update Concomitant Medication
    """
    patient_profile = get_object_or_404(PatientProfile, pk=profile_id)
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True
    )
    concomitant_medication_form = ConcomitantMedicationForm(request.POST or None, patient_profile=patient_profile)

    if request.method == "POST":
        if concomitant_medication_form.is_valid():
            concomitant_medication = concomitant_medication_form.save(commit=False)
            concomitant_medication.patient_profile = patient_profile
            concomitant_medication.drug_inn = (
                concomitant_medication_form.cleaned_data.get("drug_inn").capitalize() # type: ignore
            )
            concomitant_medication.save()

    return HttpResponseRedirect(
        reverse("patient:update_patient_profile", kwargs={"profile_id": profile_id})
    )


@user_passes_test(is_verified_doctor, login_url="accounts:user_profile")
def delete_concomitant_medication(request, profile_id, medication_id):
    patient_profile = get_object_or_404(PatientProfile, pk=profile_id)
    consent = get_object_or_404(
        Consent, doctor=request.user, patient=patient_profile.patient_user, signed=True
    )
    concomitant_medication = get_object_or_404(ConcomitantMedication, pk=medication_id)
    concomitant_medication.delete()

    return HttpResponseRedirect(
        reverse("patient:update_patient_profile", kwargs={"profile_id": profile_id})
    )
