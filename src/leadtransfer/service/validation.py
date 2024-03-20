from datetime import datetime

from django.conf import settings

from pydantic import BaseModel, field_validator


class ContactCreationData(BaseModel):
    phone: str
    email: str
    date: str
    site: str
    city: str
    page: str

    @field_validator("phone")
    def phone_validator(cls, value):
        remove_symbols = "+_-() "
        for symbol in remove_symbols:
            value = value.replace(symbol, "")
        if value[0] == 8:
            value[0] = 7
        return value


def get_contact_validated_data(data: dict) -> ContactCreationData:
    # TODO: is there always only 1 contact and 1 email?
    return ContactCreationData(
        phone=data.get("phones", [""])[0],
        email=data.get("mails", [""])[0],
        date=datetime.now().strftime("%d.%m.%Y, %H:%M:%S"),
        site=data.get("site", ""),
        city=data.get("city", ""),
        page=data.get("page", ""),
    )


class LeadCreationData(BaseModel):
    utm_source: str
    utm_medium: str
    utm_campaign: str
    utm_content: str
    utm_term: str
    roistat_visit: str


def get_lead_validated_data(data: dict) -> LeadCreationData:
    return LeadCreationData(
        utm_source=data.get("utm", dict()).get("utm_source", ""),
        utm_medium=data.get("utm", dict()).get("utm_medium", ""),
        utm_campaign=data.get("utm", dict()).get("utm_campaign", ""),
        utm_content=data.get("utm", dict()).get("utm_content", ""),
        utm_term=data.get("utm", dict()).get("utm_term", ""),
        roistat_visit=data.get("roistat_visit", ""),
    )


def get_phone_from_fields(custom_fields_values):
    for custom_field in custom_fields_values:
        if custom_field["field_id"] == settings.AMO_CONTACT_FIELD_IDS["phone"]:
            return custom_field["values"][0]["value"]
    return ""


def validate_phone(phone: str):
    remove_symbols = "+_-() "
    for symbol in remove_symbols:
        phone = phone.replace(symbol, "")
    if phone[0] == 8:
        phone[0] = 7
    return phone


def get_contact_list_validated_data(contacts: list):
    validated_contacts = []
    for contact in contacts:
        if "custom_fields_values" in contact and contact["custom_fields_values"]:
            phone = get_phone_from_fields(contact["custom_fields_values"])
            if phone:
                validated_contacts.append({
                    "contact_id": contact["id"],
                    "phone": validate_phone(phone),
                })
    return validated_contacts
