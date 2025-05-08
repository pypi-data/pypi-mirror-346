from django.conf import settings
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeletableModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        editable=False,
        on_delete=models.PROTECT,
    )
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()
    available_objects = SoftDeleteManager()

    def delete(self, actor=None, soft=True, *args, **kwargs):
        if soft:
            deleted_date = timezone.now()
            self.__class__.objects.filter(pk=self.pk).update(is_deleted=True, deleted_at=deleted_date, deleted_by=actor)
        else:
            super().delete(*args, **kwargs)

    class Meta:
        abstract = True
