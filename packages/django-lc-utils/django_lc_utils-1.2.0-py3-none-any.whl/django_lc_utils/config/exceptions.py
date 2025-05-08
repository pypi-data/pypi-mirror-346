import logging
from uuid import uuid4

import sentry_sdk
from django.conf import settings
from django.core.exceptions import ValidationError as CoreValidationError
from django.db import IntegrityError
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _
from django_error_reporting.utils import add_event_tag
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.fields import get_error_detail
from rest_framework.response import Response
from rest_framework.views import exception_handler

LOGGER = logging.getLogger("root")


def fmt_error_msg(
    err_code="F1111", usr_msg=None, tech_msg=None, instance_id=None, exc_obj=None, display_uniqueid=False
):
    uniqueid = str(uuid4())  # this will be used to filter in Sentry
    instance_id = str(instance_id) if instance_id is not None else ""

    if usr_msg is None:
        usr_msg = _("An unspecified error has occurred.  No further details at this time.")
        display_uniqueid = True
    elif not isinstance(usr_msg, str) and not isinstance(usr_msg, Promise):
        usr_msg = _("An invalid error message format was received.  No further details at this time.")
        display_uniqueid = True

    msg_to_display = f"{err_code} - {usr_msg}"
    if display_uniqueid is True:
        msg_to_display = f"{err_code} - {usr_msg}  -  ID: {uniqueid}"

    if tech_msg is None:
        if isinstance(usr_msg, str):
            tech_msg = usr_msg
        else:
            tech_msg = "No specific technical details are available."

    if tech_msg != "" and isinstance(tech_msg, str):
        sentry_msg = f"{tech_msg} - Instance: {instance_id}" if instance_id != "" else tech_msg

    else:
        sentry_msg = "tech_msg is either missing or a non-string object.  No further details at this time."

    add_event_tag("err_code", err_code)
    add_event_tag("uniqueId", uniqueid)

    sentry_sdk.capture_message(sentry_msg)

    if exc_obj is not None:
        sentry_sdk.capture_exception(exc_obj)

    return msg_to_display


def flatten_drf_validations(errors, path=None):
    if path:
        path = path.replace("_", " ").title()

    errors_list = []
    if isinstance(errors, str):
        return [f"{path} - {errors}" if path else errors]

    if isinstance(errors, list):
        for error in errors:
            errors_list = errors_list + flatten_drf_validations(error, path=path)
        return errors_list

    if isinstance(errors, dict):
        for key, val in errors.items():
            new_path = f"{path} - {key}" if path else key
            errors_list = errors_list + flatten_drf_validations(val, path=new_path)
        return errors_list


class CustomError(APIException):
    status_code = 400
    default_detail = "An error has occurred. Please validate your submission values."

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        if "status_code" in kwargs:
            self.status_code = kwargs["status_code"]


class Http404Exception(APIException):
    status_code = 404
    default_detail = "Object does not exist."


class PermissionDeniedError(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action"


def APIExceptionHandler(exc, context):
    # handle django core ValidationErrors
    if isinstance(exc, CoreValidationError):
        if hasattr(exc, "message_dict"):
            detail = exc.message_dict
        elif hasattr(exc, "message"):
            detail = exc.message
        elif hasattr(exc, "messages"):
            detail = exc.messages
        else:
            detail = get_error_detail(exc)

        exc = ValidationError(detail=detail)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response and hasattr(response, "data") and isinstance(response.data, dict):
        response.data = flatten_drf_validations(response.data)

    try:
        uid = context["request"].session["trace_id"]
    except Exception:
        uid = uuid4()

    # if there is an IntegrityError and the error response hasn't already been generated
    if isinstance(exc, IntegrityError) and not response:
        response = Response({"message": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    # If its an unhandled exception (ie 500) show a proper json response with a trace id
    if response is None and settings.DEBUG is False:
        response = Response(
            {"trace_id": str(uid), "error": True, "content": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        sentry_sdk.capture_exception(exc)
    except Exception as excp:
        LOGGER.exception(f"Error: [{excp}]")

    return response
