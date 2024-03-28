import json
import logging
from datetime import datetime

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import CRMContactSerializer
from ..service.amocrm import send_lead_to_amocrm
from ..service.validation import get_lead_validated_data, get_contact_validated_data

logger = logging.getLogger(__name__)

# class SyncContactsAPIView(ListAPIView):
#     serializer_class = CRMContactSerializer
#     queryset = CRMContact.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         data_len = 0
#         page = 1
#         while True:
#             try:
#                 contacts = get_amo_contacts(page=page)
#                 serializer = CRMContactSerializer(data=contacts, many=True)
#                 if serializer.is_valid():
#                     serializer.save()
#                 data_len += len(serializer.data)
#             except JSONDecodeError as e:
#                 break
#             except Exception as e:
#                 print(e)
#             print(page)
#             page += 1
#         return Response(data={"len": data_len}, status=status.HTTP_200_OK)


class LeadTransferAPIView(CreateAPIView):
    serializer_class = CRMContactSerializer

    def post(self, request, *args, **kwargs):
        validated_contact = get_contact_validated_data(request.data)
        validated_deal = get_lead_validated_data(request.data)
        logger.info(f"request_data: {request.data}\n"
                    f"request_time: {datetime.now()}\n"
                    f"validated_contact: {validated_contact}\n"
                    f"validated_deal: {validated_deal}\n")
        send_lead_to_amocrm(
            validated_contact,
            validated_deal
        )
        return Response(status=status.HTTP_200_OK)
