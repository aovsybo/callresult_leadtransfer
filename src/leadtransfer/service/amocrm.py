from datetime import datetime

import requests

from django.conf import settings

from . import db
from .validation import ContactCreationData, LeadCreationData


# TODO: check if token expire time is less then an hour from current moment
def get_access_token():
    url = f"https://{settings.WR_INTEGRATION_SUBDOMAIN}.amocrm.ru/oauth2/access_token"
    data = {
        "client_secret": settings.WR_INTEGRATION_CLIENT_SECRET,
        "client_id": settings.WR_INTEGRATION_CLIENT_ID,
        "refresh_token": settings.WR_REFRESH_TOKEN,
        "redirect_uri": settings.WR_INTEGRATION_REDIRECT_URI,
        "grant_type": "refresh_token",
    }
    return requests.post(url, data=data).json()["access_token"]


# TODO: replace body in request with method "get_custom_fields_values", get all fields ids
def get_custom_fields_values(fields: dict):
    custom_fields_values = []
    for field_id, field_value in fields.items():
        custom_fields_values.append({
            "field_id": field_id,
            "values": [{"value": field_value}]
        })


def create_contact(data: ContactCreationData):
    body = [{
        "name": "Идентификация с сайта daigo.ru",
        "custom_fields_values": [
            {
                "field_code": "PHONE",
                "values": [{"value": data.phone}]
            },
            {
                "field_code": "EMAIL",
                "values": [{"value": data.email}]
            },
            {
                "field_id": 794014,
                "values": [{"value": data.date}]
            },
            {
                "field_id": 784770,
                "values": [{"value": data.site}]
            },
            {
                "field_id": 612396,
                "values": [{"value": data.city}]
            },
            {
                "field_id": 794016,
                "values": [{"value": data.page}]
            },
        ]
    }]
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    url = f"https://{settings.WR_INTEGRATION_SUBDOMAIN}.amocrm.ru/api/v4/contacts"
    response = requests.post(url, json=body, headers=headers)
    return response.json()['_embedded']['contacts'][0]['id']


def get_or_create_contact(validated_data):
    if db.contact_exists(validated_data.phone):
        contact_id = db.get_contact_id_by_phone(validated_data.phone)
    else:
        contact_id = create_contact(validated_data)
        db.create_contact(contact_id=contact_id, phone=validated_data.phone)
    return contact_id


def create_lead(contact_id, data: LeadCreationData):
    body = [{
        "name": "Лид с сайта daigo.ru",
        "pipeline_id": 7566897,
        "status_id": 62668613,
        "_embedded": {
            "contacts": [{"id": contact_id}]
        },
        "custom_fields_values": [
            {
                "field_id": 166045,
                "values": [{"value": data.utm_source}]
            },
            {
                "field_id": 166043,
                "values": [{"value": data.utm_medium}]
            },
            {
                "field_id": 166047,
                "values": [{"value": data.utm_campaign}]
            },
            {
                "field_id": 166051,
                "values": [{"value": data.utm_content}]
            },
            {
                "field_id": 166049,
                "values": [{"value": data.utm_term}]
            },
            {
                "field_id": 754509,
                "values": [{"value": data.roistat_visit}]
            },
        ]
    }]
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    url = f"https://{settings.WR_INTEGRATION_SUBDOMAIN}.amocrm.ru/api/v4/leads"
    return requests.post(url, json=body, headers=headers).json()


def get_contacts():
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
    }
    url = f"https://{settings.WR_INTEGRATION_SUBDOMAIN}.amocrm.ru/api/v4/contacts"
    return requests.get(url, headers=headers)


def send_lead_to_amocrm(contact_validated_data, lead_validated_data):
    contact_id = get_or_create_contact(contact_validated_data)
    create_lead(contact_id, lead_validated_data)
