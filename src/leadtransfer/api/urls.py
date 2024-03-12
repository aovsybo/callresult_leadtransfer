from django.urls import path

from .views import TestAPI, LeadTransferAPIView

urlpatterns = [
    path('tests/', TestAPI.as_view(), name='tests'),
    path('lead-transfer/', LeadTransferAPIView.as_view(), name='lead_transfer'),
]
