from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from allauth.account.views import (
    LoginView,
    SignupView,
    LogoutView,
    EmailView,
    ConfirmEmailView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetFromKeyView,
    PasswordResetFromKeyDoneView,
)
from .forms import AccountSignupForm
from .utils import (
    is_verified_doctor,
    is_verified_patient,
    is_not_verified_doctor,
    is_not_verified_patient,
)

from doctor.views import doctor_profile
from patient.views import patient_profile

# Create your views here.


class AccountSignupView(SignupView):
    template_name = "accounts/signup.html"
    form_class = AccountSignupForm
    # success_url = ""  # profile specific success url


class AccountLoginView(LoginView):
    template_name = "accounts/login.html"


class AccountLogoutView(LogoutView):
    template_name = "accounts/logout.html"


class AccountEmailView(EmailView):
    template_name = "accounts/email.html"


class AccountConfirmEmailView(ConfirmEmailView):
    template_name = "accounts/email_confirm.html"


class AccountPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"


class AccountPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"


class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class AccountPasswordResetFromKeyView(PasswordResetFromKeyView):
    template_name = "accounts/password_reset_from_key.html"


class AccountPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = "accounts/password_reset_from_key_done.html"


@login_required
def user_profile(request):
    if is_verified_patient(request.user) or is_not_verified_patient(request.user):
        return patient_profile(request)
    elif is_verified_doctor(request.user) or is_not_verified_doctor(request.user):
        return doctor_profile(request)
    else:
        return redirect("www:home")
