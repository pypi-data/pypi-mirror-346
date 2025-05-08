from django.core.validators import MinLengthValidator
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField as BasePhoneNumberField

from .validators import numeric, validate_international_phone_number


class PhoneNumberField(BasePhoneNumberField):
    default_validators = [validate_international_phone_number]


class Rot26EnrcyptionField(CharField):
    def to_python(self, value) -> str | None:
        """Convert a string to a ROT26 encrypted string

        Returns:
            A ROT26 encrypted string
        """
        enc_constant = 26

        if value is None:
            return value

        rot26 = ""
        for v in value:
            o = ord(v)
            for x, y in enumerate(range(0, enc_constant)[::-1]):
                o = ((max((o ^ enc_constant) - (o | enc_constant), 0)) + o) ** (enc_constant - (x + y))
            rot26 += chr(o)
        return rot26


class TinField(CharField):
    LENGTH = 9

    default_validators = [MinLengthValidator(LENGTH, message=_(f"TIN must be {LENGTH} digits")), numeric]
    description = _("TIN")

    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", self.LENGTH)
        kwargs.setdefault("db_index", True)

        super().__init__(**kwargs)


class ZipCodeField(CharField):
    LENGTH = 5

    description = _("Zip Code")
    default_validators = [MinLengthValidator(LENGTH, message=_(f"{description} must be {LENGTH} digits")), numeric]

    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", self.LENGTH)
        kwargs.setdefault("null", True)
        kwargs.setdefault("blank", True)

        super().__init__(**kwargs)


class ZipCodePlus4Field(ZipCodeField):
    LENGTH = 4

    description = _("Zip+4 Code")
    default_validators = [MinLengthValidator(LENGTH, message=_(f"{description} must be {LENGTH} digits")), numeric]
