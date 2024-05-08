from django.urls import path
from . import views

app_name = "doctor"

urlpatterns = [
    path("update/", views.update_doctor_profile, name="update_doctor_profile"),
    path("<str:profile_id>/", views.doctor_profile, name="doctor_profile"),
    path("<str:profile_id>/approve/", views.approve_doctor, name="approve_doctor")
]