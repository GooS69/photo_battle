from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.post_serializers import PostListSerializer
from post.api.v1.my_serializers.user_serializers import UsersListSerializer, UsersRequest
from post.api.v1.services.user.list import UsersService
from post.api.v1.services.user.user_posts import UserPostsService


class UsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(query_serializer=UsersRequest(), responses={200: 'ok'})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UsersService, {})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return self.paginate(outcome.result, request)

    def paginate(self, queryset, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = 'page_size'
        paginated_outcome = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(UsersListSerializer(paginated_outcome, many=True).data)


class UserPostsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserPostsService, {'user_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return self.paginate(outcome.result, request)

    def paginate(self, queryset, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_size_query_param = 'page_size'
        paginated_outcome = paginator.paginate_queryset(queryset, request)
        return paginator.get_paginated_response(PostListSerializer(paginated_outcome, many=True).data)