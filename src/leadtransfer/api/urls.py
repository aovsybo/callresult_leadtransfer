from django.urls import path

from .views import TestAPI, LeadTransferAPIView, SyncContactsAPIView

urlpatterns = [
    path('tests/', TestAPI.as_view(), name='tests'),
    path('sync-contacts/', SyncContactsAPIView.as_view(), name='sync-contacts'),
    path('lead-transfer/', LeadTransferAPIView.as_view(), name='lead_transfer'),
]
