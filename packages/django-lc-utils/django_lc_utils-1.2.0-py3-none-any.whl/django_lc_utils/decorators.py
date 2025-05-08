from functools import wraps

from django.apps import apps
from django.contrib.auth.management import create_permissions
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


def lender_view(view_func):
    """
    Decorator for making sure lender routes are only accessed through Lender Portal
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_borrower:
            return redirect("/")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def borrower_view(view_func):
    """
    Decorator for making sure borrower routes are only accessed through Borrower Portal
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_borrower:
            return redirect("/")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def tenant_migration(*args, tenant_schema=True, public_schema=False):
    """
    Decorator to control which schemas a data migration will execute under.
    If `tenant_schema=True`, the data migration will execute on non-public schemas.
    If `public_schema=True`, the data migration will execute on the public schema.
    """

    def _tenant_migration(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _, schema_editor = args  # noqa
            except Exception as excp:
                raise Exception(f"Decorator requires apps & schema_editor as positional arguments: [{excp}]")

            result = None
            if (tenant_schema is True and schema_editor.connection.schema_name != get_public_schema_name()) or (
                public_schema is True and schema_editor.connection.schema_name == get_public_schema_name()
            ):
                result = func(*args, **kwargs)

            return result  # return value for testing purposes

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return _tenant_migration(args[0])

    return _tenant_migration


def migrate_permissions(app_label=None):
    """
    Ensures the permissions for a given app (or all apps) are migrated before running a data migration.
    Args:
        app_label : Label of the app to force permissions to migrate; if none, performs all apps. Defaults to None.
    """

    def _migrate_permissions(func):
        def wrapper(*args, **kwargs):
            configs = apps.get_app_configs() if app_label is None else [apps.get_app_config(app_label)]

            for app_config in configs:
                app_config.models_module = True
                create_permissions(app_config, verbosity=0)
                app_config.models_module = None

            func(*args, **kwargs)

        return wrapper

    return _migrate_permissions
