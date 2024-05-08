from django.urls import path
from . import views

app_name = "trial"

urlpatterns = [
    path("all/", views.view_all_trials, name="view_all_trials"),
    path("all/personal/", views.enrolled_patients, name="enrolled_patients"),
    path("<str:trial_id>/", views.trial, name="trial"),
]
