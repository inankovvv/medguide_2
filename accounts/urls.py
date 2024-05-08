from django.urls import path, re_path
from . import views
from doctor import views as doctor_views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.AccountSignupView.as_view(), name="account_signup"),
    path("login/", views.AccountLoginView.as_view(), name="account_login"),
    path("logout/", views.AccountLogoutView.as_view(), name="account_logout"),
    path("email/", views.AccountEmailView.as_view(), name="account_email"),
    path(
        "confirm-email/<str:key>/",
        views.AccountConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "password/change/",
        views.AccountPasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path(
        "password/reset/",
        views.AccountPasswordResetView.as_view(),
        name="account_reset_password",
    ),
    path(
        "password/reset/done/",
        views.AccountPasswordResetDoneView.as_view(),
        name="account_reset_password_done",
    ),
    re_path(
        r"password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.AccountPasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        views.AccountPasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/update/", doctor_views.update_doctor_profile, name="update_doctor_profile"),
]
