from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from .serializers import CRMContactSerializer
from ..service.amocrm import send_lead_to_amocrm
from ..service.validation import get_lead_validated_data, get_contact_validated_data


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
        return Response(status=status.HTTP_200_OK)
