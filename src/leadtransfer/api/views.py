from json import JSONDecodeError

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
        data_len = 0
        page = 1000
        while True:
            try:
                contacts = get_amo_contacts(page=page)
            except JSONDecodeError as e:
                break
            serializer = CRMContactSerializer(data=contacts, many=True)
            if serializer.is_valid():
                serializer.save()
            data_len += len(serializer.data)
            page += 1
        return Response(data={"len": data_len}, status=status.HTTP_200_OK)


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
