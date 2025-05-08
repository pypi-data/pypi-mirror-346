import logging

from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django_tenants.utils import get_public_schema_name

from .paginators import FastPaginator

IS_POPUP_VAR = "_popup"
TO_FIELD_VAR = "_to_field"

LOGGER = logging.getLogger("root")


class AutoCompleteAdminMixin(admin.ModelAdmin):
    AUTOCOMPLETE_FIELD_TYPES = [
        "ForeignKey",
        "ManyToManyField",
    ]

    def get_autocomplete_field_types(self):
        return self.AUTOCOMPLETE_FIELD_TYPES

    def get_autocomplete_fields(self, request):
        autocomplete_fields = list(super().get_autocomplete_fields(request))

        for field in self.model._meta.get_fields():
            if type(field).__name__ not in self.get_autocomplete_field_types():
                continue

            try:
                admin_class = admin.site._registry[field.related_model]
                if not hasattr(admin_class, "search_fields") or not admin_class.search_fields:
                    # Skip if no search_fields present (throws an exception)
                    continue
            except Exception as excp:
                # Just Logging the exception
                LOGGER.debug(f"Error: [{excp}]")

            autocomplete_fields.append(field.name)

        return autocomplete_fields


class FastPaginationModelAdmin(AutoCompleteAdminMixin):
    paginator = FastPaginator
    show_full_result_count = False


class PublicTenantOnlyAdmin(TenantAdminMixin, FastPaginationModelAdmin):
    """
    Hides public models from tenants.
    django_tenants.middleware.main.TenantMainMiddleware adds a tenant attribute if a schema is found but does not add if it is the public schema
    """

    def has_view_permission(self, request, *args, view=None, **kwargs):
        return not hasattr(request, "tenant") or request.tenant.schema_name == get_public_schema_name()

    def has_add_permission(self, request, *args, view=None, **kwargs):
        return not hasattr(request, "tenant") or request.tenant.schema_name == get_public_schema_name()

    def has_change_permission(self, request, *args, view=None, **kwargs):
        return not hasattr(request, "tenant") or request.tenant.schema_name == get_public_schema_name()

    def has_delete_permission(self, request, *args, view=None, **kwargs):
        return not hasattr(request, "tenant") or request.tenant.schema_name == get_public_schema_name()

    def has_view_or_change_permission(self, request, *args, view=None, **kwargs):
        return not hasattr(request, "tenant") or request.tenant.schema_name == get_public_schema_name()
