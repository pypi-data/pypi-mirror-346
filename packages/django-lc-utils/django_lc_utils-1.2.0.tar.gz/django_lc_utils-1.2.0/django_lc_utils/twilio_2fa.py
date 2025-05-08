from constance import config
from django_tenants.utils import (
    get_public_schema_name,
    get_tenant_model,
    schema_context,
)
from django_twilio_2fa.utils import get_setting, get_twilio_client

__all__ = ["create_twilio_verify_service"]


def create_twilio_verify_service(schema_name, friendly_name=None, force=False, use_existing=True):
    tenant = None

    if schema_name != get_public_schema_name():
        tenant = get_tenant_model().objects.get(schema_name=schema_name)

    # Twilio credential check
    if not get_setting("ACCOUNT_SID"):
        return (
            False,
            "Twilio credentials are not available. Set TWILIO_2FA_ACCOUNT_SID and TWILIO_2FA_AUTH_TOKEN settings.",
        )

    # Set friendly name
    if not friendly_name and tenant:
        friendly_name = str(tenant)
    elif not friendly_name:
        friendly_name = "LOS"

    with schema_context(schema_name):
        # Check for existing config
        has_verify_sid = config.TWILIO_2FA_SERVICE_ID != ""

        if has_verify_sid and not force:
            return (False, f"Twilio Verify service ID is already set for {schema_name}")

        twilio = get_twilio_client()

        # Check for existing service
        existing_service_sid = None

        if use_existing:
            print(f"Searching for Twilio Verify service with friendly name: {friendly_name}")
            services = twilio.verify.v2.services.list(limit=100, page_size=100)

            for service in services:
                if service.friendly_name != friendly_name:
                    continue

                existing_service_sid = service.sid
                break

        if existing_service_sid:
            config.TWILIO_2FA_SERVICE_ID = existing_service_sid

            return (True, f"Set Twilio Verify service for {schema_name} with existing SID: {existing_service_sid}")

        service = twilio.verify.v2.services.create(friendly_name=friendly_name)

        config.TWILIO_2FA_SERVICE_ID = service.sid

        return (True, f"Created new Twilio Verify service for {schema_name}: {config.TWILIO_2FA_SERVICE_ID}")
