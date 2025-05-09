"""
project: IBT24/25, xkubec03
author: Viktor Kubec
file: urls.py

brief:
This file defines routing for each plugin view.
"""

from django.urls import path

from .views import CableCreateView, CableExtensionEditView

app_name = 'cable_extension'

urlpatterns = [
    path('cable/create/', CableCreateView.as_view(), name='cable_create'),
    path('extension/<int:pk>/edit/', CableExtensionEditView.as_view(), name='cableextension_edit'),
]
