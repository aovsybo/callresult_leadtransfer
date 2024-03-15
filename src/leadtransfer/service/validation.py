from datetime import datetime

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
        utm_source=data["utm"]["utm_source"],
        utm_medium=data["utm"]["utm_medium"],
        utm_campaign=data["utm"]["utm_campaign"],
        utm_content=data["utm"]["utm_content"],
        utm_term=data["utm"]["utm_term"],
        roistat_visit=data["roistat_visit"],
    )
