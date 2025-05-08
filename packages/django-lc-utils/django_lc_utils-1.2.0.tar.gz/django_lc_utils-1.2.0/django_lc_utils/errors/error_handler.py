import json

from django.utils.translation import gettext_lazy as _

from ..config.exceptions import fmt_error_msg


class ErrorCode:
    __slots__ = ("data", "error_codes_path")

    def __init__(self, error_codes_file_path):
        self.error_codes_path = error_codes_file_path

        with open(self.error_codes_path) as file:
            self.data = json.loads(file.read())

    def error_message(self, error_code, data=None, exception_object=None, display_uniqueid=False, instance_id=None):
        user_message = self.data[error_code]["usr_msg"]
        tech_message = self.data[error_code]["tech_msg"]

        if data:
            user_message = user_message.format(**data)
            tech_message = tech_message.format(**data)

        translated_user_message = _(user_message)

        return fmt_error_msg(
            err_code=error_code,
            usr_msg=translated_user_message,
            tech_msg=tech_message,
            exc_obj=exception_object,
            display_uniqueid=display_uniqueid,
            instance_id=instance_id,
        )
