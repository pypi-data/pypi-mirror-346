import os
import re

import magic
import phonenumber_field.phonenumber
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django_lc_utils.errors.error_manager import error

from .config.exceptions import fmt_error_msg

NUMERIC_PATTERN = r"[^0-9\s]"
alphanumeric_pattern = r"[^a-zA-Z0-9\s]"
numeric_pattern = r"[^0-9\s]"
numeric = RegexValidator(r"^\d*$", "Numeric Values Required")
decimal = RegexValidator(r"^\d*[.]?\d*$", "Decimal Values Required")
alphanumeric = RegexValidator(r"^[a-zA-Z0-9]*$", "Must Be Alphanumeric", code="alphanumeric")


VALID_KINDS = {
    "json": [
        "ASCII text",
        "JSON data",
    ],
    "jpg": [
        "JPEG image data",
    ],
    "jpeg": [
        "JPEG image data",
    ],
    "png": [
        "PNG image data",
    ],
    "csv": [
        "ASCII text",
    ],
    "pdf": [
        "PDF document",
    ],
    "xlsx": [
        "Microsoft Excel 2007+",
    ],
    "docx": [
        "Microsoft Word 2007+",
    ],
    # glitch w < Office 2007 docs .. xls and doc will not report correctly.
    # reports "Composite Document File V2 Document" instead
    "xls": [
        "Microsoft Excel 2003",
    ],
    "doc": [
        "Microsoft Word 2003",
    ],
    "pfx": [
        "data",
    ],
}


def validate_excel_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".xls", ".xlsx", ".csv"]
    if ext.lower() not in valid_extensions:
        raise ValidationError(error.error_message("E0001"))


def validation_logic(value, magic_buffer_size, valid_kinds):
    ext_from_filename = os.path.splitext(value.name)[1].lower()[1:]
    ext_from_filename = "jpg" if ext_from_filename == "jpeg" else ext_from_filename  # conform jpg/jpeg
    expected_kind = valid_kinds.get(ext_from_filename)
    kind = magic.from_buffer(value.read(magic_buffer_size)).split(",")[0]
    if (expected_kind is None) or (kind not in expected_kind and kind != "Composite Document File V2 Document"):
        raise ValidationError(error.error_message("E0002"))
    elif kind == "Composite Document File V2 Document":
        # special case -  glitch w < Office 2007 docs.  validate further
        special_magic = bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1])
        # same string for all office docs so ppt pub or visio could slip through,  cannot differentiate between doc/xls
        value.seek(0)
        if value.read(len(special_magic)) != special_magic:
            raise ValidationError(error.error_message("E0003"))


def validate_file_extension(value):
    """
    Determine if file has appropriate extension and type.  Refactord to use python-magic module to check buffered
    contents rather than trust extension or trust header mime type.  For Office docs < Office 2007, further validation
    done with magic numbeers string due to reported type glitch
    https://pypi.org/project/python-magic/
    """
    magic_buffer_size = 2048
    valid_kinds = VALID_KINDS.copy()

    validation_logic(value, magic_buffer_size, valid_kinds)


def validate_file_extension_zip(value):
    """
    validate_file_extension function with the addition of zip file to VALID_KINDS
    """
    magic_buffer_size = 2048
    valid_kinds = VALID_KINDS.copy()
    valid_kinds.update(
        {
            "zip": [
                "Zip archive data",
            ]
        }
    )
    validation_logic(value, magic_buffer_size, valid_kinds)


def values_within_tolerance(val1, val2, tolerance=None, tolerance_pct=None):
    """
    Determine if val1 and val2 are the same or within the provided tolerances.
    If tolerance and tolerance_pct aren't provided, no tolerance will be allowed
    """
    val1 = float(val1 or 0)
    val2 = float(val2 or 0)
    tolerance = float(tolerance or 0)
    tolerance_pct = float(tolerance_pct or 0)

    if val1 and val1 > 0:
        variance1 = abs(round(float(val2) - float(val1), 2)) / float(val1)
    else:
        variance1 = 1

    variance2 = abs(float(val1) - float(val2))

    if variance1 <= tolerance_pct or round(variance2, 2) <= tolerance:
        return True

    return False


def validate_no_html_tags(value):
    html_matches = re.findall("^(?:.*<[^>]+>).*", value)
    if len(html_matches):
        err_code = "E1100"
        usr_msg = _("No HTML tags allowed in field.")
        tech_msg = "No HTML tags allowed in field."
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)


def validate_no_nested_html(value):
    if not value:
        return

    if isinstance(value, (list, tuple, set)):
        for nested_value in value:
            validate_no_nested_html(nested_value)
    elif isinstance(value, dict):
        for key, nested_value in value.items():
            validate_no_html_tags(str(key))
            validate_no_nested_html(nested_value)
    else:
        validate_no_html_tags(str(value))


def validate_phone_number(phone_number):
    phone_number = phone_number.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if phone_number and not len(phone_number) == 10:
        err_code = "E1101"
        usr_msg = _("Phone number must be 10 digits")
        tech_msg = "Phone number must be 10 digits"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)
    if re.findall(NUMERIC_PATTERN, phone_number):
        err_code = "E1102"
        usr_msg = _("Phone Number is Invalid")
        tech_msg = "Phone Number is Invalid"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)

    try:
        if "+1" not in phone_number:
            phone_number = f"+1 {phone_number}"
        phonenumbers.parse(phone_number)
    except Exception:
        err_code = "E1103"
        usr_msg = _("Phone Number is Invalid")
        tech_msg = "Phone Number is Invalid"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)


def validate_international_phone_number(phone_number):
    if not phone_number:
        return
    try:
        phonenumber_field.phonenumber.PhoneNumber.from_string(phone_number)
    except Exception:
        err_code = "E1103"
        usr_msg = _("Phone Number is Invalid")
        tech_msg = "Phone Number is Invalid"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)


def validate_max_80_length(field):
    if (len(field) + (len(re.findall(alphanumeric_pattern, field)))) > 80:
        err_code = "E1104"
        usr_msg = _("Must be less than 80 characters (non-alphanumeric characters will count as 2 characters)")
        tech_msg = "Must be less than 80 characters (non-alphanumeric characters will count as 2 characters)"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)


def validate_domain(value):
    regex = re.compile(
        # r"^(?:http|ftp)s?://" # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        # domain...
        r"localhost|" r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # localhost...
        # ...or ip
        # r"(?::\d+)?" # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    if re.match(regex, str(value)) is None:
        err_code = "E1105"
        usr_msg = _("Invalid domain provided")
        tech_msg = "Invalid domain provided"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)

    invalid_schemes = ["http://", "https://", "www."]
    if any(scheme in value for scheme in invalid_schemes):
        err_code = "E1106"
        usr_msg = _("Do not include any of the following in the domain: {}").format(invalid_schemes)
        tech_msg = f"Do not include any of the following in the domain: {invalid_schemes}"
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)

    return value


def alphanumeric_with_underscore(value):
    reg = re.compile("^[a-zA-Z0-9_]*$")
    if not reg.match(value):
        raise ValidationError("Only Alphanumeric/underscore(_) is allowed")


def validate_cif_file_extension(value):
    """
    Determine if file has appropriate extension and type.  Refactord to use python-magic module to check buffered
    contents rather than trust extension or trust header mime type.  For Office docs < Office 2007, further validation
    done with magic numbeers string due to reported type glitch
    https://pypi.org/project/python-magic/
    """
    magic_buffer_size = 2048
    valid_kinds = {
        "txt": "ASCII text",
        "csv": "ASCII text",
    }

    ext_from_filename = os.path.splitext(value.name)[1].lower()[1:]
    expected_kind = valid_kinds.get(ext_from_filename)
    kind = magic.from_buffer(value.read(magic_buffer_size)).split(",")[0]
    if kind != expected_kind:
        err_code = "E1501"
        usr_msg = _("Unsupported/invalid file extension.")
        tech_msg = "Unsupported/invalid file extension."
        error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
        raise ValidationError(error_msg)
