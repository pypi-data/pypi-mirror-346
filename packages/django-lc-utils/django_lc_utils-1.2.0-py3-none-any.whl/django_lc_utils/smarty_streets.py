import logging

import sentry_sdk
from django.conf import settings
from smartystreets_python_sdk import ClientBuilder, StaticCredentials, exceptions
from smartystreets_python_sdk.us_autocomplete import Lookup as AutocompleteLookup
from smartystreets_python_sdk.us_extract import Lookup as ExtractLookup
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

LOGGER = logging.getLogger("root")


class SmartyStreets:
    def __init__(self):
        if not settings.SMARTY_STREETS_AUTH_ID or not settings.SMARTY_STREETS_AUTH_TOKEN:
            e = Exception("Smarty Street Credentials NOT set")
            sentry_sdk.capture_exception(e)
            return e

        credentials = StaticCredentials(settings.SMARTY_STREETS_AUTH_ID, settings.SMARTY_STREETS_AUTH_TOKEN)
        self.client = ClientBuilder(credentials).build_us_street_api_client()
        self.auto_complete_client = ClientBuilder(credentials).build_us_autocomplete_api_client()
        self.extract_client = ClientBuilder(credentials).build_us_extract_api_client()

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-street-api#input-fields
    def address_lookup(
        self,
        addressee=None,
        street=None,
        street2=None,
        secondary=None,
        urbanization=None,
        city=None,
        state=None,
        zipcode=None,
        candidates=5,
        match="invalid",
    ):
        if not street or not state:
            return

        lookup = StreetLookup()
        # lookup.input_id = "24601"  # Optional ID from your system
        lookup.addressee = addressee
        lookup.street = street
        lookup.street2 = street2
        lookup.secondary = secondary
        lookup.urbanization = urbanization  # Only applies to Puerto Rico addresses
        lookup.city = city
        lookup.state = state
        lookup.zipcode = zipcode
        lookup.candidates = candidates
        lookup.match = match  # "invalid" is the most permissive match,
        # this will always return at least one result even if the address is invalid.
        # Refer to the documentation for additional Match Strategy options.

        try:
            self.client.send_lookup(lookup)
        except exceptions.SmartyException as err:
            sentry_sdk.capture_exception(err)

        addresses = []
        for address in lookup.result:
            temp_address = address.__dict__
            temp_address["components"] = address.components.__dict__
            temp_address["metadata"] = address.metadata.__dict__
            temp_address["analysis"] = address.analysis.__dict__
            try:
                del temp_address["analysis"]["is_ews_match"]
            except Exception as excp:
                LOGGER.exception(f"Error: [{excp}]")
            addresses.append(temp_address)

        return addresses

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/us-autocomplete-api#http-request-input-fields
    def auto_complete_address_lookup(self, address_string, city_filter=None, state_filter=None, max_suggestions=5):
        lookup = AutocompleteLookup(address_string)
        if city_filter:
            lookup.add_city_filter = city_filter
        if state_filter:
            lookup.add_state_filter = state_filter
        lookup.max_suggestions = max_suggestions

        try:
            self.auto_complete_client.send(lookup)
        except exceptions.SmartyException as err:
            sentry_sdk.capture_exception(err)

        addresses = []
        for suggestion in lookup.result:
            addresses.append(suggestion.__dict__)
        return addresses

    # Documentation for input fields can be found at:
    # https://smartystreets.com/docs/cloud/us-extract-api#http-request-input-fields
    def extract_address(
        self,
        address_string,
        aggressive=True,
        addresses_have_line_breaks=False,
        addresses_per_line=1,
    ):
        lookup = ExtractLookup()
        lookup.text = address_string
        lookup.aggressive = aggressive
        lookup.addresses_have_line_breaks = addresses_have_line_breaks
        lookup.addresses_per_line = addresses_per_line

        try:
            addresses = self.extract_client.send(lookup).addresses
        except exceptions.SmartyException as err:
            sentry_sdk.capture_exception(err)

        for address in addresses:
            if address.verified and len(address.candidates) == 1:
                return address.candidates[0].components.__dict__

        return None
