from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.my_serializers.post_serializers import PostListRequest, PostListSerializer, UserPostListRequest
from post.api.v1.services.post_list.user_posts import UserPostListService
from post.api.v1.services.post_list.verified_posts import VerifiedPostListService


class VerifiedPostList(APIView):

    @swagger_auto_schema(query_serializer=PostListRequest,
                         responses={200: PostListSerializer})
    def get(self, request, *args, **kwargs):
        try:
            filter = request.query_params['filter']
        except KeyError:
            filter = None

        outcome = ServiceOutcome(VerifiedPostListService, {'filter': filter, 'ordering': request.query_params['ordering']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(PostListSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)


class UserPostList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(query_serializer=UserPostListRequest,
                         responses={200: PostListSerializer})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UserPostListService,{'user': request.user, 'status': request.query_params['status']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(PostListSerializer(outcome.result, many=True).data, status=status.HTTP_200_OK)