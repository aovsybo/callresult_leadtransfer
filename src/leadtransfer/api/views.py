from json import JSONDecodeError

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

from .serializers import CRMContactSerializer
from ..models import CRMContact
from ..service.amocrm import send_lead_to_amocrm, get_amo_contacts, test_fw
from ..service.validation import get_lead_validated_data, get_contact_validated_data


class SyncContactsAPIView(ListAPIView):
    serializer_class = CRMContactSerializer
    queryset = CRMContact.objects.all()

    def get(self, request, *args, **kwargs):
        data_len = 0
        page = 1
        while True:
            try:
                contacts = get_amo_contacts(page=page)
                serializer = CRMContactSerializer(data=contacts, many=True)
                if serializer.is_valid():
                    serializer.save()
                data_len += len(serializer.data)
            except JSONDecodeError as e:
                break
            except Exception as e:
                print(e)
            print(page)
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
        test_fw()
        return Response(data=data, status=status.HTTP_200_OK)
