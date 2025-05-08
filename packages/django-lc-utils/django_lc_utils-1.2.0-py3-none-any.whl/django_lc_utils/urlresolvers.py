from django.conf import settings
from django.db import connection
from django.urls import resolve, reverse
from django.utils.functional import lazy
from django_tenants.utils import get_public_schema_name


def get_urlconf():
    if connection.schema_name == get_public_schema_name():
        return settings.TENANT_TYPES["public"]["URLCONF"]
    elif connection.schema_name == "filemover":
        return settings.TENANT_TYPES["filemover"]["URLCONF"]
    else:
        return settings.TENANT_TYPES["organization"]["URLCONF"]


def custom_reverse(viewname, url_conf=None, args=None, kwargs=None, current_app=None):
    """
    Custom reverse function for tenant-aware url resolving
    """
    url_conf = get_urlconf() if url_conf is None else url_conf

    return reverse(  # nosemgrep
        viewname,
        urlconf=url_conf,
        args=args,
        kwargs=kwargs,
        current_app=current_app,
    )


custom_reverse_lazy = lazy(custom_reverse, str)


def custom_resolve(path, urlconf=None):
    """
    Custom function for tenant-aware url resolving
    """
    if urlconf is None:
        urlconf = get_urlconf()
    return resolve(path, urlconf=urlconf)
