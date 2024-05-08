from django.urls import path
from . import views

app_name = "files_app"

urlpatterns = [
    path("view/<str:file_id>/", views.view_file, name="view_file"),
    path("upload/", views.upload_file, name="upload_file"),
    path("upload/multiple/", views.upload_multiple_files, name="upload_multiple_files"),
]
