from rest_framework import status, viewsets
from rest_framework.response import Response

from .mixins import ReadReplicaMixin


# FIXME: Add and fix readreplicamixin
class BorrowerPermissionModelViewSet(ReadReplicaMixin, viewsets.ModelViewSet):
    borrower_http_methods = ["get", "post"]

    def is_valid_user(self, request):
        if request.user.is_authenticated is False or (
            request.user.is_borrower
            and request.method.lower() not in map(lambda x: x.lower(), self.borrower_http_methods)
        ):
            return False

        return True

    def create(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.is_valid_user(request) is False:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return super().destroy(request, *args, **kwargs)
