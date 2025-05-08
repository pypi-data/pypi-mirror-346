import traceback
import uuid
import warnings
from collections import OrderedDict

import semantic_version
import structlog
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import EmptyResultSet, ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import ManyToOneRel, OneToOneRel, QuerySet
from django.db.models.fields import (
    BigIntegerField,
    DecimalField,
    FloatField,
    IntegerField,
    PositiveSmallIntegerField,
)
from django.db.models.fields.json import JSONField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils.managers import QueryManager
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from semantic_version.django_fields import VersionField

# from los.auditlog.models import LogEntry
from .config.exceptions import fmt_error_msg

STRUCTLOGGER = structlog.get_logger(__name__)


class InvalidOperation(Exception):
    pass


class SlightlySaferSoftDeletableQuerySetMixin:
    """
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``is_removed`` field to True.
    """

    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        # TODO: uncomment this statement when ready to deprecate
        # raise InvalidOperation("Calling delete here is not allowed! Use `bulk_delete` on the Model")

        warnings.warn(
            "Calling delete is going to be deprecated in future! Use `bulk_delete` on the Model class",
            DeprecationWarning,
        )

        return self.unsafe_delete()

    def unsafe_delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        tb = str(traceback.extract_stack())
        try:
            qry = str(self.query)
        except EmptyResultSet:
            qry = "***** EMPTY QUERYSET *****"

        from los.requests.tasks import create_bulk_delete_audit_event
        from los.utils.celery import queue_task

        content_type = ContentType.objects.get_for_model(self.model)
        content_type_id = content_type.id
        object_ids = list(map(str, self.values_list("id", flat=True)))

        if not object_ids:
            return 0

        STRUCTLOGGER.info(
            "Queueing the celery task for creating bulk delete audit events",
            object_ids=object_ids,
            content_type_id=content_type_id,
        )

        queue_task(
            create_bulk_delete_audit_event,
            object_ids=object_ids,
            content_type_id=content_type_id,
            queue="audit_log_queue",
            countdown=3,
            traceback_stack=tb,
            str_queryset=qry,
        )

        # still doing this operation here because many of our APIs do a bulk delete followed by a DB call to do other updates
        fields_to_update = {"is_removed": True}

        if hasattr(content_type, "modified"):
            fields_to_update["modified"] = timezone.now()

        result = self.update(**fields_to_update)

        STRUCTLOGGER.info(
            "Processed a bulk soft delete operation",
            model=content_type.app_labeled_name,
            object_id=object_ids[0],
        )

        return result


class SlightlySaferSoftDeletableQuerySet(SlightlySaferSoftDeletableQuerySetMixin, QuerySet):
    pass


class SlightlySaferSoftDeletableManagerMixin:
    """
    Manager that limits the queryset by default to show only not removed
    instances of model.
    """

    _queryset_class = SlightlySaferSoftDeletableQuerySet

    def __init__(self, *args, _emit_deprecation_warnings=False, **kwargs):
        self.emit_deprecation_warnings = _emit_deprecation_warnings
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """

        if self.emit_deprecation_warnings:
            warning_message = (
                "{0}.objects model manager will include soft-deleted objects in an "
                "upcoming release; please use {0}.available_objects to continue "
                "excluding soft-deleted objects. See "
                "https://django-model-utils.readthedocs.io/en/stable/models.html"
                "#softdeletablemodel for more information."
            ).format(self.model.__class__.__name__)
            warnings.warn(warning_message, DeprecationWarning)

        kwargs = {"model": self.model, "using": self._db}
        if hasattr(self, "_hints"):
            kwargs["hints"] = self._hints

        return self._queryset_class(**kwargs).filter(is_removed=False)


class SlightlySaferSoftDeletableManager(SlightlySaferSoftDeletableManagerMixin, models.Manager):
    pass


class SoftDeleteMixin(models.Model):
    is_removed = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    objects = SlightlySaferSoftDeletableManager()
    deleted = QueryManager(is_removed=True)
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if (self._state.adding or self.pk is None) and hasattr(self, "created"):
            # reset the created date if it's already set for a new object being added
            self.created = timezone.now()

        super().save(*args, **kwargs)

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self._force_save = True  # pass _force_save in case the model supports it
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    @classmethod
    def bulk_delete(cls, **kwargs):
        """Slightly safer bulk soft delete.  This method attempts to ensure that no argument passed to it is `None`.
        Instead, if you really intend to filter by `None`, you should use `field__isnull=True`.

        We'll probably want to do this for other methods like `filter` and `exclude` as well, because we have run into
        scenarios where filtering on the value of a nullable FK from another model has caused some bad results too

        will also need a way to exclude fields

        kwargs only allowed for now...no Q objects, but we should be able to call Q.deconstruct() and loop through
        any child Q objects to determine if we received a `field = None` query
        """
        if not kwargs:
            raise InvalidOperation("Filters cannot be blank")

        for key, value in kwargs.items():
            if value is None:
                raise InvalidOperation("Cannot filter by None.  Must use `__isnull=True`")

        STRUCTLOGGER.info("Executing a bulk soft delete operation", klass=cls, arguments=kwargs)
        cls.objects.filter(**kwargs).unsafe_delete()  # nosemgrep


class VersionMixin(models.Model):
    version = VersionField(editable=False, default="1.0.0")
    version_major = models.IntegerField(editable=False, null=True)
    version_minor = models.IntegerField(editable=False, null=True)
    version_patch = models.IntegerField(editable=False, null=True)

    class Meta:
        abstract = True

    # current_version = QueryManager(is_removed=False)
    # deleted = QueryManager(is_removed=True)
    # all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if isinstance(self.version, str):
            self.version = semantic_version.Version(self.version)
        self._sync_version_parts()
        return super().save(*args, **kwargs)

    def _sync_version_parts(self):
        if self.version:
            self.version_major = self.version.major
            self.version_minor = self.version.minor
            self.version_patch = self.version.patch


class JsonSerializeMixin:
    def model_to_dict(self, return_fk_as_id=False):
        serialized_model = {}
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if (
                value is False
                or value is True
                or value is None
                or type(field) in [BigIntegerField, FloatField, IntegerField, PositiveSmallIntegerField]
            ):
                serialized_model[field.name] = value
            elif type(field) == DecimalField:
                serialized_model[field.name] = float(value) if value else None
            elif type(field) == ForeignKey and return_fk_as_id:
                if isinstance(value.pk, uuid.UUID):
                    serialized_model[f"{field.name}_id"] = str(value.pk)
                else:
                    serialized_model[f"{field.name}_id"] = value.pk
            elif isinstance(field, JSONField):
                serialized_model[field.name] = value
            else:
                serialized_model[field.name] = str(value)

        for relation in self._meta.related_objects:
            if hasattr(relation.related_model, "model_to_dict"):
                serialized_model[relation.name] = []
                if hasattr(self, relation.name):
                    if type(relation) == OneToOneRel:
                        serialized_model[relation.name] = getattr(self, relation.name).model_to_dict()
                    # elif type(getattr(self, relation.name)) == ManyToOneRel:
                    elif type(relation) == ManyToOneRel:
                        for obj in getattr(self, relation.name).all():
                            serialized_model[relation.name].append(obj.model_to_dict())

        return serialized_model


# TODO: THIS USES THE LOS AUDIT LOG MODELS, SO LOOK AT HOW COULD WE IMPLEMENT THIS.

# class LoggingMixin:
#     def save_and_log(self, request=None, action=LogEntry.Action.UPDATE, log_as_task=False, extras=None, **kwargs):
#         if extras is None:
#             extras = {}
#         changes = {}
#         for key, value in kwargs.items():
#             if str(getattr(self, key)) != str(value):
#                 changes[key] = [str(getattr(self, key)), str(value)]
#                 setattr(self, key, value)

#         if request:
#             actor = request.user
#             ip = get_client_ip(request)
#         else:
#             actor = None
#             ip = None

#         if extras:
#             changes.update(extras)

#         self.save()
#         if log_as_task:
#             LogEntry.objects.log_create_as_task(
#                 instance=self,
#                 action=action,
#                 actor=actor,
#                 changes=changes,
#                 remote_addr=ip,
#             )
#         else:
#             LogEntry.objects.log_create(
#                 instance=self,
#                 action=action,
#                 actor=actor,
#                 changes=changes,
#                 remote_addr=ip,
#             )


class MutuallyExclusiveSerializerMixin(serializers.Serializer):
    """The Highlander of serializer validators"""

    MUTUALLY_EXCLUSIVE_FIELDS = []
    REQUIRED = "required"  # Required means one or the other of the fields is required
    OPTIONAL = "optional"  # Optional means the field is optional, but if provided, only one can be set
    EXCLUSIVITY_TYPE = REQUIRED

    def validate(self, attrs, *args, **kwargs):
        if self.MUTUALLY_EXCLUSIVE_FIELDS:
            populated = 0
            for field in self.MUTUALLY_EXCLUSIVE_FIELDS:
                if attrs.get(field, None):
                    populated += 1

            if self.EXCLUSIVITY_TYPE == self.REQUIRED:
                if populated != 1:
                    err_code = "E1092"
                    usr_msg = _("Exactly one of the following fields must be set: {}").format(
                        self.MUTUALLY_EXCLUSIVE_FIELDS
                    )
                    tech_msg = f"Exactly one of the following fields must be set: {self.MUTUALLY_EXCLUSIVE_FIELDS}"
                    error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
                    raise ValidationError(error_msg)
            elif self.EXCLUSIVITY_TYPE == self.OPTIONAL:
                if populated > 1:
                    err_code = "E1093"
                    usr_msg = _("Only one of the following fields can be set: {}").format(
                        self.MUTUALLY_EXCLUSIVE_FIELDS
                    )
                    tech_msg = f"Only one of the following fields can be set: {self.MUTUALLY_EXCLUSIVE_FIELDS}"
                    error_msg = fmt_error_msg(err_code=err_code, usr_msg=usr_msg, tech_msg=tech_msg)
                    raise ValidationError(error_msg)

        return super().validate(attrs, *args, **kwargs)


class DataMaskingSerializerMixin(serializers.Serializer):
    """
    Mask PII or other sensitive information
        - mask_field - Hook to write custom masking function if needed
        - unmask_fields - Hook to write custom permissions if needed. DEFAULT: Mask sensitive fields for loans in non-editable status.
          NOTE: Request context must be passed to serializer to check for user perms
    """

    class Meta:
        SENSITIVE_FIELDS = []

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance, *args, **kwargs)
        self.UNMASK_FIELDS = self.unmask_fields(instance, *args, **kwargs)

    def unmask_fields(self, instance, *args, **kwargs):
        """
        Hook to add custom logic for any scenarios where the fields need to be unmasked.
        NOTE: Request context must be passed to serializer to check for user perms
        """
        return bool(kwargs.get("context", {}).get("unmask_fields", False))

    def mask_field(self, value, *args, **kwargs):
        """Hook to write custom masking function if needed"""
        return self.dynamic_mask_account_number(value)

    @staticmethod
    def dynamic_mask_account_number_last_four(account_number):
        if not account_number:
            return account_number
        account_number = str(account_number).strip()
        return account_number[:-4] + "XXXX"

    @staticmethod
    def dynamic_mask_account_number(account_number):
        if not account_number:
            return account_number
        account_number = str(account_number)
        length = len(account_number)
        masked = ""
        if length > 4:
            last_displayed_digits = 4
        else:
            last_displayed_digits = 1

        last_digits = account_number[-last_displayed_digits:]
        for i in range(length - last_displayed_digits):
            if account_number[i].isalnum():
                masked += "X"
            else:
                masked += account_number[i]  # keep delimiter(s)
        return masked + last_digits

    @staticmethod
    def mask_account_number(account_number):
        if account_number is None:
            return account_number
        account_number = str(account_number)
        last_four = account_number[-4:]
        masked = ""
        for i in range(len(account_number) - 4):
            if account_number[i].isalnum():
                masked += "X"
            else:
                masked += account_number[i]  # keep delimiter(s)
        return masked + last_four

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                value = field.to_representation(attribute)
                if self.UNMASK_FIELDS is False and field.field_name in self.Meta.SENSITIVE_FIELDS:
                    value = self.mask_field(value, field_name=field.field_name)
                ret[field.field_name] = value
        return ret


class DontUpdateModelSerializerMixin:
    @staticmethod
    def needs_saving(data_dict, instance_dict):
        for k, v in data_dict.items():
            if k in instance_dict and instance_dict[k] != v:
                return True
        return False

    def dont_update(self, instance, validated_data):
        # same as update() except no instance.save()
        # serializers.raise_errors_on_nested_writes('update', self, validated_data)
        # info = model_meta.get_field_info(instance)

        # m2m_fields = []
        # for attr, value in validated_data.items():
        #     if attr in info.relations and info.relations[attr].to_many:
        #         m2m_fields.append((attr, value))
        #     else:
        #         setattr(instance, attr, value)

        # for attr, value in m2m_fields:
        #     field = getattr(instance, attr)
        #     field.set(value)

        return instance


class CopyMixin(models.Model):
    copied_from = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="copies")
    copied_data = models.JSONField(
        "JSON of values copied from Original", blank=True, null=True, encoder=DjangoJSONEncoder
    )

    class Meta:
        abstract = True


class ProtectedFieldsModelMixin:
    @cached_property
    def old_version(self):
        return self.__class__.objects.filter(pk=self.pk).first()

    def is_protected_fields_modified(self, protected_fields, interface, return_modified_fields: bool = False):
        if not interface:
            if return_modified_fields:
                return True, []

            return True

        return interface.parameters_changed(self.get_protected_fields_values(protected_fields), return_modified_fields)

    def get_protected_fields_values(self, protected_fields):
        return {field: getattr(self, field) for field in protected_fields}

    def validate_interfaces(self, *args, **kwargs):
        raise NotImplementedError


# class ReadReplicaMixin:
#     """
#     ModelViewSet mixin to force list/retrieve methods to the replica db
#     """

#     def use_read_replica(self, request, *args, **kwargs) -> bool:
#         """
#         Determines if queries in the scope of the given request
#         should use the read replica.
#         Args:
#             request (Request): The HTTP request
#         Returns:
#             bool: Whether this request should use the read replica.
#         """
#         return request.method.lower() == "get"

#     def dispatch(self, request, *args, **kwargs):
#         """Builtin dispatch method for a DRF ModelViewSet.
#         This is where we are overriding all GET methods to use the read replica.

#         Args:
#             request (HttpRequest): request object

#         Returns:
#             response (HttpResponse, JsonResponse): Response object
#         """
#         new_request = self.initialize_request(request, *args, **kwargs)
#         if self.use_read_replica(new_request, *args, **kwargs):
#             with use_replica_db:
#                 return super().dispatch(request, *args, **kwargs)
#         return super().dispatch(request, *args, **kwargs)
