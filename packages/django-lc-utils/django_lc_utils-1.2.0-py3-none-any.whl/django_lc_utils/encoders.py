import semantic_version
from django.core.serializers.json import DjangoJSONEncoder


class VersionCompatibleEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, semantic_version.Version):
            return str(obj)
        return super().default(obj)
