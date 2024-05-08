from django.urls import path
from . import views

app_name = "ecrf"

urlpatterns = [
    path("<str:ecrf_id>/", views.ecrf, name="ecrf"),
    path("<str:trial_id>/<int:patient_id>/", views._ecrf, name="_ecrf"),
    path("<str:ecrf_id>/visit/new/", views.create_visit, name="create_visit"),
]
