import phonenumbers
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def formatted_phone_number(phone_number, format=None, region=None):
    """Template tag to format a phone number in various formats.

    Args:
        phone_number (str | PhoneNumber): The phone number to format.
        format (str, optional): The target phone number format, one of "E164", "INTERNATIONAL", "NATIONAL", "RFC3966".
            Defaults to None, which will use the application default.
        region (str, optional): The region of the source phone number, if not in E164 format.
            Defaults to None, which will use the application default.

    Returns:
        str: The phone number in the target format.
    """
    if not phone_number:
        return None

    if not format:
        format = getattr(settings, "PHONENUMBER_DEFAULT_FORMAT", None)
    else:
        format = getattr(phonenumbers.PhoneNumberFormat, format, None)

    if not format:
        return phone_number

    if not region:
        region = getattr(settings, "PHONENUMBER_DEFAULT_REGION", None)

    if not isinstance(phone_number, phonenumbers.PhoneNumber):
        phone_number = str(phone_number)
        phone_number = phonenumbers.parse(number=phone_number, region=region)

    return phonenumbers.format_number(phone_number, format)
