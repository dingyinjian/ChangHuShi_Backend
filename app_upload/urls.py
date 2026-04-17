# fileupload/urls.py
from django.urls import path
from .views import SingleFileUploadView, MultipleFileUploadView

urlpatterns = [
    path('upload/', SingleFileUploadView.as_view(), name='single-file-upload'),
    path('upload/multiple/', MultipleFileUploadView.as_view(), name='multiple-file-upload'),
]