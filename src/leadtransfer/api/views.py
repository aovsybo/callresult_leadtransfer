from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from .serializers import CRMContactSerializer
from ..models import CRMContact
from ..service.amocrm import send_lead_to_amocrm, get_amo_contacts
from ..service.validation import get_lead_validated_data, get_contact_validated_data


class SyncContactsAPIView(ListAPIView):
    serializer_class = CRMContactSerializer
    queryset = CRMContact.objects.all()

    def get(self, request, *args, **kwargs):
        contacts = get_amo_contacts()
        serializer = CRMContactSerializer(data=contacts, many=True)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LeadTransferAPIView(CreateAPIView):
    serializer_class = CRMContactSerializer

    def post(self, request, *args, **kwargs):
        send_lead_to_amocrm(
            get_contact_validated_data(request.data),
            get_lead_validated_data(request.data)
        )
        return Response(status=status.HTTP_200_OK)


class TestAPI(ListAPIView):
    def get(self, request, *args, **kwargs):
        data = dict()
        return Response(data=data, status=status.HTTP_200_OK)
