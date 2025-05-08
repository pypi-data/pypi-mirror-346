import abc
import hashlib
from collections import OrderedDict

import sentry_sdk
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import InvalidPage, Page, Paginator
from django.db.models.query import QuerySet
from django.utils.functional import cached_property
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response


class BaseFastPaginator(metaclass=abc.ABCMeta):
    TIMEOUT = getattr(settings, "FAST_PAGINATION_TIMEOUT", 360)
    PREFIX = getattr(settings, "FAST_PAGINATION_PREFIX", "fastpagination")

    @abc.abstractmethod
    def count(self):
        raise NotImplementedError

    @abc.abstractmethod
    def page(self, number):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_page(self, *args, **kwargs):
        raise NotImplementedError


class FastQuerysetPaginator(Paginator, BaseFastPaginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

        try:
            encoded_query = str(object_list.query).encode("utf-8")
            raw_query_key = hashlib.md5(encoded_query, usedforsecurity=False).hexdigest()
            self.cache_pks_key = f"{self.PREFIX}:pks:{raw_query_key}"
            self.cache_count_key = f"{self.PREFIX}:count:{raw_query_key}"
        except Exception:
            encoded_query = None

    @property
    def count(self):
        try:
            result = cache.get(self.cache_count_key)
        except Exception:
            return 0
        if result is None:
            result = self.object_list.count()

            cache.set(self.cache_count_key, result, timeout=self.TIMEOUT)

        return result

    @property
    def pks(self):
        result = cache.get(self.cache_pks_key)
        if result is None:
            result = self.object_list.values_list("pk", flat=True)
            cache.set(self.cache_pks_key, result, timeout=self.TIMEOUT)
        return result

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        pks = self.pks[bottom:top]
        object_list = self.object_list.filter(pk__in=pks)
        return self._get_page(object_list, number, self)

    def _get_page(self, *args, **kwargs):
        return FastQuerysetPage(*args, **kwargs)


class FastObjectPaginator(Paginator, BaseFastPaginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, cache_key=None):
        if cache_key is None:
            raise ValueError("You should provide cache_key" + "for your results")
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)
        self.cache_count_key = f"{self.PREFIX}:count:{cache_key}"

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        object_list = self.object_list[bottom:top]
        return self._get_page(object_list, number, self)

    @property
    def count(self):
        result = cache.get(self.cache_count_key)
        if result is None:
            result = len(self.object_list)
            cache.set(self.cache_count_key, result, timeout=self.TIMEOUT)
        return result

    def _get_page(self, *args, **kwargs):
        return FastObjectPage(*args, **kwargs)


class FastPaginator:
    def __new__(cls, *args, **kwargs):
        object_list = args[0]
        if isinstance(object_list, QuerySet):
            return FastQuerysetPaginator(*args, **kwargs)
        return FastObjectPaginator(*args, **kwargs)


class FastQuerysetPage(Page):
    def __len__(self):
        return len(self.paginator.ids)


class FastObjectPage(Page):
    def __len__(self):
        return len(self.paginator.object_list)


class RecklessPaginator(Paginator):
    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        return 999999999


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param], strict=True, cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                return self.max_page_size  # return max page size if we receive a negative number

        return self.page_size


class FasterPageNumberPagination(StandardResultsSetPagination):
    django_paginator_class = FastPaginator

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return 0
        self._page_size = page_size

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        self.page_number = page_number

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(page_number=page_number, message=str(exc))
            sentry_sdk.capture_exception(Exception(msg))
            raise NotFound("Page not found")

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_next_num(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()

    def get_previous_num(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_current_num(self):
        try:
            n = int(self.page_number)
        except Exception:
            n = None
        return n

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("current", self.get_current_num()),
                    ("next", self.get_next_link()),
                    ("next_num", self.get_next_num()),
                    ("page_size", self._page_size),
                    ("previous", self.get_previous_link()),
                    ("previous_num", self.get_previous_num()),
                    ("results", data),
                ]
            )
        )
