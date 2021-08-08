from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils.permissions import PostPermission
from post.api.v1.my_serializers.post_serializers import CreatePostSerializer, PostListSerializer, PostListRequest
from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.services.post.create import PostCreateService
from post.api.v1.services.post.delete import PostDeleteService
from post.api.v1.services.post.get import PostGetService
from post.my_models.post import Post


class CreatePostView(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreatePostSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PostCreateService,
                                 {
                                    'user': request.user,
                                    'name': request.data.get('name')
                                 },
                                 request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class DeletePostView(APIView):
    permission_classes = [PostPermission, ]

    @swagger_auto_schema(responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PostDeleteService, {'user': request.user, 'post_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PostGetService, {'post_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(PostListSerializer(outcome.result).data, status=status.HTTP_200_OK)
