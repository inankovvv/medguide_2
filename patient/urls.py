from django.urls import path
from . import views

app_name = "patient"

# Important - patient profile view is in accounts under user_profile

urlpatterns = [
    path("<str:profile_id>/", views.patient_profile, name="patient_profile"),
    path(
        "<str:profile_id>/update/",
        views.update_patient_profile,
        name="update_patient_profile",
    ),
    path(
        "<str:profile_id>/update/medcondition/",
        views.update_medical_condition,
        name="update_medical_condition",
    ),
    path(
        "<str:profile_id>/delete/medcondition/<int:condition_id>/",
        views.delete_medical_condition,
        name="delete_medical_condition",
    ),
    path(
        "<str:profile_id>/update/conmed/",
        views.update_concomitant_medication,
        name="update_concomitant_medication",
    ),
    path(
        "<str:profile_id>/delete/conmed/<int:medication_id>/",
        views.delete_concomitant_medication,
        name="delete_concomitant_medication",
    ),
]
