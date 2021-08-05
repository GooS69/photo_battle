from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.v1.my_serializers.post_serializers import CreatePostSerializer, PostListSerializer
from post.api.v1.services.PostShowService import PostShowService
from post.api.utils.service_outcome import ServiceOutcome
from post.my_models.post import Post


class CreatePost(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreatePostSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(name=request.POST.get('name'), img=self.request.FILES.get('img'), owner=self.request.user)
        return Response()


class GetPost(APIView):

    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(PostShowService, kwargs)
        if bool(outcome.errors):
            return Response(outcome.errors, outcome.response_status or status.HTTP_400_BAD_REQUEST)
        return Response(PostListSerializer(outcome.result).data)


class DeletePost(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.delete()
        return Response()


class VerifiedPostList(APIView):

    @swagger_auto_schema(manual_parameters=[Parameter(name='filter', in_=IN_QUERY, type='str', default=''), ],
                         responses={200: PostListSerializer})
    def get(self, request, *args, **kwargs):
        filter = request.GET.get('filter') if request.GET.get('filter') else ''
        posts = Post.objects.all().filter(status='verified', name__icontains=filter)
        return Response(PostListSerializer(posts, many=True).data)


class UserPostsList(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(manual_parameters=[Parameter(name='status',
                                                      in_=IN_QUERY,
                                                      type='str',
                                                      enum=['verified', 'not_verified', 'rejected'],
                                                      default='verified'), ],
                         responses={200: PostListSerializer})
    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        posts = Post.objects.all().filter(status=status, owner=request.user)
        return Response(PostListSerializer(posts, many=True).data)