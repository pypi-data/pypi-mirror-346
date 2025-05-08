from django.conf import settings

if not settings.configured:
    settings.configure(
        SMARTY_STREETS_AUTH_ID="test_auth_id",
        SMARTY_STREETS_AUTH_TOKEN="test_auth_token",
    )
