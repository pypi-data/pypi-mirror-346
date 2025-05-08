import phonenumbers
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.serializerfields import PhoneNumberField as BasePhoneNumberField
from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` and/or `exclude` argument that
    control which fields should be displayed (or not). Also supports double underscore
    notation for nested serializers.

    Excludes take precedence if a field is present in both `fields` and `exclude`

    Example Usage:

    serializer = DynamicFieldsModelSerializer(
        fields=['id', 'user', 'name', 'updated'],
        exclude=['user__address']
    )

    This would only include `id`, `user`, `name`, `updated`, and `user.address` would be removed
    """

    def __init__(self, *args, **kwargs):
        def parse_nested_fields(fields, exclude=False):
            field_object = {"fields": []}
            for f in fields:
                obj = field_object
                nested_fields = f.split("__")
                for v in nested_fields:
                    if v not in obj["fields"]:
                        obj["fields"].append(v)
                    if nested_fields.index(v) < len(nested_fields) - 1:
                        obj[v] = obj.get(v, {"fields": []})
                        obj = obj[v]
            return field_object

        def select_nested_fields(serializer, fields, exclude=False):
            for k in fields:
                if str(k).lower() == "fields":
                    if exclude:
                        fields_to_exclude(serializer, fields[k], fields.keys())
                    else:
                        fields_to_include(serializer, fields[k])
                else:
                    select_nested_fields(serializer.fields[k], fields[k], exclude)

        def fields_to_include(serializer, fields):
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(serializer.fields.keys())
            for field_name in existing - allowed:
                serializer.fields.pop(field_name, None)

        def fields_to_exclude(serializer, fields, ignore):
            # Drop any fields that ARE specified in the `fields` argument.
            for field_name in fields:
                if field_name not in ignore:
                    serializer.fields.pop(field_name, None)

        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude = kwargs.pop("exclude", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            fields = parse_nested_fields(fields)
            select_nested_fields(self, fields)

        if exclude is not None:
            exclude = parse_nested_fields(exclude, exclude=True)
            select_nested_fields(self, exclude, exclude=True)


class PhoneNumberField(BasePhoneNumberField):
    def __init__(self, format=phonenumbers.PhoneNumberFormat.E164, **kwargs):
        self.format = format
        super().__init__(**kwargs)

    def to_representation(self, value: PhoneNumber):
        if not value:
            return None

        return value.format_as(self.format)
