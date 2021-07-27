from django.views.generic.detail import SingleObjectMixin
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.v1.my_serializers.comment_serializers import CommentSerializer
from post.api.v1.my_serializers.post_serializers import CreatePostSerializer, PostListSerializer
from post.my_models.comment import Comment
from post.my_models.post import Post


class CreatePost(APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreatePostSerializer, responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        post = Post.objects.create(name=request.POST.get('name'), img=self.request.FILES.get('img'), owner=self.request.user)
        return Response()


class DeletePost(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    model = Post

    @swagger_auto_schema(responses={200: 'ok'})
    def delete(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        post.delete()
        return Response()


class PostList(APIView):

    @swagger_auto_schema(responses={200: PostListSerializer})
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        return Response(PostListSerializer(posts, many=True).data)
