from datetime import timedelta

import requests
from django.core.cache import cache
from django.utils import timezone
from requests.auth import HTTPBasicAuth
from requests.exceptions import (
    ConnectionError,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    Timeout,
    TooManyRedirects,
)
from rest_framework import status

# User properties
# https://docs.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0#properties


class MicrosoftGraph:
    access_token = None
    access_token_expiration = None

    def __init__(self, tenant_id, client_id, secret_key):
        self.tenant_id = tenant_id
        self.auth_url_base = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0"

        self.basic_auth = HTTPBasicAuth(client_id, secret_key)

        self.load_credentials()
        self.connection_exceptions = (
            ConnectionError,
            ProxyError,
            ReadTimeout,
            SSLError,
            Timeout,
            TooManyRedirects,
        )

    def get_manager(self, user_id, log_config):
        # user_id is either the UUID or userPrincipalName
        # https://docs.microsoft.com/en-us/graph/api/user-list-manager?view=graph-rest-1.0&tabs=http

        response = self.execute("get", f"users/{user_id}/manager", log_config)

        return response

    def get_users(self, log_config):
        # user_id is either the UUID or userPrincipalName
        # https://docs.microsoft.com/en-us/graph/api/user-list-manager?view=graph-rest-1.0&tabs=http
        # https://graph.microsoft.com/v1.0/users?$select=id,displayName,mail,jobTitle,mobilePhone,officeLocation,surname,givenName,department&$expand=manager($select=displayName,mail)
        response = self.execute(
            "get",
            "users/?$select=id,displayName,mail,jobTitle,mobilePhone,officeLocation,surname,givenName,department&$expand=manager($select=id,displayName,mail)",
            log_config,
        )

        return response

    def create_user(self, payload, log_config):
        # user_id is either the UUID or userPrincipalName
        # https://docs.microsoft.com/en-us/graph/api/user-list-manager?view=graph-rest-1.0&tabs=http

        response = self.execute("post", "users", log_config, json=payload)

        # if response.status_code == status.HTTP_201_CREATED:
        #     return response.json()

        return response

    def assign_manager(self, payload, user_id, log_config):
        return self.execute("put", f"users/{user_id}/manager/$ref", log_config, json=payload)

    def get_user_manager(self, user_principle_name=None, user_id=None, log_config=None, params=None):
        # GET /me/manager
        # GET /users/{id | userPrincipalName}/manager
        if user_principle_name is None and user_id is None:
            return None
        if user_principle_name:
            url = f"users/{user_principle_name}/manager"
        else:
            url = f"users/{user_id}/manager"

        response = self.execute("get", url, log_config, params=params)

        return response

    def get_user(self, user_principle_name=None, user_id=None, log_config=None, params=None):
        # user_id is either the UUID or userPrincipalName
        # https://docs.microsoft.com/en-us/graph/api/user-list-manager?view=graph-rest-1.0&tabs=http
        if user_principle_name is None and user_id is None:
            return None
        if user_principle_name:
            url = f"users/{user_principle_name}"
        else:
            url = f"users/{user_id}"

        response = self.execute("get", url, log_config, params=params)

        return response

    def get_all_groups(self, log_config=None):
        # user_id is either the UUID or userPrincipalName
        # https://docs.microsoft.com/en-us/graph/api/user-list-manager?view=graph-rest-1.0&tabs=http

        response = self.execute("get", "groups?$select=id,displayName", log_config)

        payload = response.json()
        del payload["@odata.context"]

        return payload

    def get_group_owners(self, group_id, log_config=None):
        # GET /groups/{id}/owners
        response = self.execute("get", f"groups/{group_id}/owners", log_config)

        return response

    def get_user_groups(self, user_principle_name=None, user_id=None, log_config=None):
        # GET https://graph.microsoft.com/v1.0/users/6e7b768e-07e2-4810-8459-485f84f8f204/memberOf
        response = None
        if user_id:
            response = self.execute("get", f"users/{user_id}/memberOf", log_config)
        elif user_principle_name:
            response = self.execute("get", f"users/{user_principle_name}/memberOf", log_config)
        else:
            raise KeyError("Mandatory field user_id or user_principle_name is unavailable")

        return response

    def get_group_members(self, group_id=None, log_config=None, params=None):
        # GET https://graph.microsoft.com/v1.0/users/6e7b768e-07e2-4810-8459-485f84f8f204/memberOf
        # query_params - ?$select=displayName, id, description
        url = f"groups/{group_id}/members"
        response = self.execute("get", url, log_config, params=params)

        return response

    def add_user_to_ad_group(self, user_id=None, group_id=None, log_config=None):
        # POST /groups/{group-id}/members/$ref
        payload = {"@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"}
        response = self.execute("post", f"groups/{group_id}/members/$ref", log_config=log_config, json=payload)

        return response

    def remove_user_from_ad_group(self, user_id=None, group_id=None, log_config=None):
        response = self.execute("delete", f"groups/{group_id}/members/{user_id}/$ref", log_config=log_config)

        return response

    #
    # request utilities

    def execute(self, method, endpoint, log_config, **kwargs):
        method = method.lower()

        if not hasattr(requests, method):
            raise KeyError(f"Method is not available: {method}")

        if "headers" not in kwargs:
            kwargs["headers"] = {}

        kwargs["headers"].update({"Authorization": f"Bearer {self.get_access_token()}"})

        url = f"https://graph.microsoft.com/v1.0/{endpoint}"
        request_time = timezone.now()
        response = requests.request(method=method, url=url, **kwargs)
        log_entry = None
        try:
            if log_config:
                if response:
                    response_time = request_time + response.elapsed
                else:
                    response_time = request_time

                log_entry = log_config["model"](
                    service_request=log_config["service_request"],
                    requested_by=log_config["user"],
                    request_url=f"{method}: {url}",
                    request_headers=kwargs["headers"],
                    response_headers=response.headers if response else "",
                    request_body=kwargs["json"] if method.lower() == "post" else "",
                    request_time=request_time,
                    response_code=response.status_code,
                    response_body="" if response.status_code == status.HTTP_204_NO_CONTENT else response.json(),
                    response_time=response_time,
                    active_directory_type="AZURE",
                )
                log_entry.save()

            response.raise_for_status()
            return response
        except self.connection_exceptions as excp:
            if log_config:
                if response:
                    response_time = log_entry.request_time + response.elapsed
                else:
                    response_time = log_entry.request_time
                log_entry = log_config["model"](
                    service_request=log_config["service_request"],
                    requested_by=log_config["user"],
                    request_url=f"{method}: {url}",
                    request_headers=kwargs["headers"],
                    response_headers="",
                    request_body=kwargs["json"] if method.lower() == "post" else "",
                    request_time=request_time,
                    response_code=0,
                    response_body=excp,
                    response_time=response_time,
                    active_directory_type="AZURE",
                )
                log_entry.save()
            raise
        except HTTPError as excp:
            raise Exception(
                f"[AZURE] - Received bad response. Status code: [{response.status_code}] for [{method}: {endpoint}]. Error: [{response.text}]"
            ) from excp

    #
    # auth utilities

    def load_credentials(self):
        credentials = cache.get("ms_azure_backend_access_token")
        if credentials is None:
            return
        self.access_token = credentials.get("access_token")
        self.access_token_expiration = credentials.get("expiration")

    def save_credentials(self):
        credentials = {
            "access_token": self.access_token,
            "expiration": self.access_token_expiration,
        }
        cache.set(
            "ms_azure_backend_access_token",
            credentials,
            timeout=(self.access_token_expiration - timezone.now()).seconds,
        )

    def is_token_expired(self):
        if not self.access_token_expiration:
            return True

        return timezone.now() > self.access_token_expiration

    def get_access_token(self):
        if self.access_token and not self.is_token_expired():
            return self.access_token

        url = f"{self.auth_url_base}/token"
        response = requests.post(
            url=url,
            auth=self.basic_auth,
            data={"grant_type": "client_credentials", "scope": "https://graph.microsoft.com/.default"},
        )

        payload = response.json()

        if response.status_code in (400, 401, 404, 415):
            raise Exception(
                f"[AZURE] - Received bad response. Status code: [{response.status_code}] for [post: {url}]. Error: [{payload['error']}: {payload['error_description']}]"
            )

        self.access_token = payload.get("access_token")
        self.access_token_expiration = timezone.now() + timedelta(seconds=payload.get("expires_in"))

        self.save_credentials()

        return self.access_token
