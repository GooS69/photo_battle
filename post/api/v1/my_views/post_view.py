from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils.permissions import PostsPermissions
from post.api.v1.my_serializers.post_serializers import CreatePostSerializer, PostListSerializer, PostsRequest
from post.api.utils.service_outcome import ServiceOutcome
from post.api.v1.services.post.create import CreatePostService
from post.api.v1.services.post.delete import DeletePostService
from post.api.v1.services.post.get import ShowPostService
from post.api.v1.services.post.list import PostsService
from post.api.v1.services.post.put import UpdatePostService
from post.utils.paginator import paginate


class PostView(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @swagger_auto_schema(responses={200: 'ok'})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(ShowPostService, {'post_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(PostListSerializer(outcome.result).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CreatePostSerializer, responses={200: 'ok'})
    def put(self, request, *args, **kwargs):
        outcome = ServiceOutcome(UpdatePostService, {'post_id': kwargs['pk'],
                                                  'name': request.data.get('name')}, request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        outcome = ServiceOutcome(DeletePostService, {'user': request.user, 'post_id': kwargs['pk']})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)


class PostsView(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [PostsPermissions]

    @swagger_auto_schema(query_serializer=PostsRequest(), responses={200: PostListSerializer()})
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PostsService, {**{'user': request.user if request.user.is_authenticated else None},
                                                **request.query_params.dict()})
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return paginate(outcome.result, request, PostListSerializer)


    @swagger_auto_schema(request_body=CreatePostSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(CreatePostService, {'user': request.user, 'name': request.data.get('name')},
                                 request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)