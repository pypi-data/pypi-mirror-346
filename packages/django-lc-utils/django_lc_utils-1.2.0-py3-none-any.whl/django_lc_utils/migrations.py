import os

from django.db import ProgrammingError, connection, migrations
from django.db.models import Q
from django_tenants.migration_executors import base, multiproc, standard
from django_tenants.utils import get_public_schema_name, get_tenant_model


class TenantFieldMixin:
    def __init__(self, *args, **kwargs):
        self.create_in_public_schema = kwargs.pop("public_schema", False)
        self.create_in_tenant_schema = kwargs.pop("tenant_schema", False)
        super().__init__(*args, **kwargs)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        if (self.create_in_public_schema and connection.schema_name == get_public_schema_name()) or (
            self.create_in_tenant_schema and connection.schema_name != get_public_schema_name()
        ):
            try:
                super().database_forwards(app_label, schema_editor, from_state, to_state)
            except ProgrammingError as excp:  # sometimes it can exist
                if "already exists" not in str(excp):
                    raise


class AddTenantField(TenantFieldMixin, migrations.AddField):
    pass


class RemoveTenantField(TenantFieldMixin, migrations.RemoveField):
    pass


class AddCustomField(TenantFieldMixin, migrations.AddField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_in_tenant_schema = False


def get_db_table():
    model = get_tenant_model()
    return model.objects._meta.db_table


class BaseSoftDeleteExecutorMixin:
    def __init__(self, args, options):
        super().__init__(args, options)
        self.inactive_tenants = set()
        self.multi_inactive_tenants = set()
        tenant_table = get_db_table()
        if tenant_table in connection.introspection.table_names():
            inactive_tenants = get_tenant_model().objects.filter(Q(is_deleted=True) | Q(is_ready=False))
            self.inactive_tenants = inactive_tenants.values_list("schema_name", flat=True).distinct()
            self.multi_inactive_tenants = inactive_tenants.values_list("schema_name", "tenant_type").distinct()

    def run_migrations(self, tenants=None):
        tenants = tenants or []
        active_tenants = list(set(tenants) - self.inactive_tenants)
        super().run_migrations(tenants=active_tenants)

    def run_multi_type_migrations(self, tenants=None):
        tenants = tenants or []
        active_tenants = list(set(tenants) - self.multi_inactive_tenants)
        super().run_multi_type_migrations(tenants=active_tenants)


class MultiprocessingSoftDeleteExecutor(BaseSoftDeleteExecutorMixin, multiproc.MultiprocessingExecutor):
    codename = "multiprocessing_soft_delete"


class StandardSoftDeleteExecutor(BaseSoftDeleteExecutorMixin, standard.StandardExecutor):
    codename = "standard_soft_delete"


def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def get_executor(codename=None):
    codename = codename or os.environ.get("EXECUTOR", standard.StandardExecutor.codename)

    for klass in get_all_subclasses(base.MigrationExecutor):
        if klass.codename == codename:
            return klass

    raise NotImplementedError("No executor with codename %s" % codename)
