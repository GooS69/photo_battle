from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.user_serializers import UsersListSerializer, UsersRequest
from post.api.v1.services.user.list import UsersService
from post.utils.paginator import paginate


class UsersView(APIView):

    @swagger_auto_schema(query_serializer=UsersRequest(), responses={200: 'ok'})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UsersService, {})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return paginate(outcome.result, request, UsersListSerializer)
