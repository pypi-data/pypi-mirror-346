import os

from django_lc_utils.errors.error_handler import ErrorCode as UtilsErrorCode

error = UtilsErrorCode(error_codes_file_path=os.path.join(os.path.dirname(__file__), "error_codes.json"))
