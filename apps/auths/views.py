from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from auths.models import CustomUser


class ListUsers(APIView):
    """
    View for CustomUser.

    * Does-not equire token authentication.
    * Only superusers are able to access this view.
    """
    permission_classes: tuple = (
        permissions.IsAdminUser,
    )

    def get(self, request) -> Response:
        """Return list of all users."""

        data: list = [user.email for user in CustomUser.objects.all()]
        return Response(data)