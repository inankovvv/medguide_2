from django.urls import path
from . import views

app_name = "consent"

urlpatterns = [
    path("create/", views.create_consent, name="create_consent"),
    path("create/trial/<str:trial_id>/<int:patient_id>/", views.create_trial_consent, name="create_trial_consent"),
    path("accept/<str:consent_id>/", views.accept_consent, name="accept_consent"),
    path("accept/trial/<str:trial_consent_id>/", views.accept_trial_consent, name="accept_trial_consent"),
    path("view/<str:consent_id>/", views.view_consent, name="view_consent"),
    path("all/", views.view_all_consents, name="view_all_consents"),
    path("patients/", views.view_consented_patients, name="view_consented_patients"),
]
