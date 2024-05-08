from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.conf import settings
from accounts.models import MGUser
from accounts.utils import is_verified_doctor, is_not_verified_doctor
from .models import DoctorProfile
from .forms import UpdateDoctorProfileForm

# Create your views here.


@user_passes_test(is_verified_doctor, login_url="www:home")
def doctor_profile(request, profile_id=None):
    context = dict()
    if profile_id:
        doctor_profile = get_object_or_404(DoctorProfile, id=profile_id)
    else:
        doctor_profile = request.user.DoctorProfile
    context["doctor_profile"] = doctor_profile
    return render(request, "doctor/doctor_profile.html", context=context)


@user_passes_test(is_not_verified_doctor)
def update_doctor_profile(request):
    context = dict()
    doctor = get_object_or_404(DoctorProfile, doctor_user=request.user)
    profile_form = UpdateDoctorProfileForm(
        request.POST or None, instance=doctor or None
    )
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        if not profile.first_update:
            _notify_admin_of_doctor_first_update(profile)
            messages.info(
                request,
                "Please, note that we will contact you on the given number or email so that we can confirm your identity. We may request additional documentation to confirm your active medical license.",
            )
            messages.success(
                request,
                "Your profile was updated successfully. The team has been notified and will review your profile.",
            )
            profile.first_update = True
        else:
            messages.success(request, "Your profile was updated successfully.")
        profile.save()

    context["profile_form"] = profile_form
    return render(request, "doctor/update_doctor_profile.html", context=context)


def _notify_admin_of_doctor_first_update(profile):
    """Send an email to the admin when a new doctor account has been created."""
    subject = f"{profile} was updated for the first time"
    message = f"Dear Admin, Please note that {profile} was updated for the first time. Please, review and approve or decline request."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.DEFAULT_FROM_EMAIL,]

    send_mail(subject, message, from_email, recipient_list)


@staff_member_required
def approve_doctor(request, profile_id):
    doctor_profile = get_object_or_404(DoctorProfile, id=profile_id)
    doctor_user = get_object_or_404(MGUser, pk=doctor_profile.doctor_user.pk)
    if not doctor_user.verified:
        doctor_user.verified = True
        doctor_user.save()
        doctor_profile.first_update = True
        doctor_profile.save()
    return HttpResponseRedirect(reverse("doctor:doctor_profile", kwargs={"profile_id": profile_id}))
