from django.contrib.contenttypes.models import ContentType
from drf_yasg.openapi import Parameter, IN_QUERY, IN_BODY
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

from post.api.v1.my_serializers.comment_serializers import CreateCommentSerializer, CommentSerializer
from post.my_models.comment import Comment
from post.my_models.post import Post


class CreateComment(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @swagger_auto_schema(request_body=CreateCommentSerializer,
                         responses={201: 'ok'})
    def post(self, request, *args, **kwargs):
        if request.data['content_type'] == 'post':
            parent = Post.objects.get(pk=request.data['object_id'])
        elif request.data['content_type'] == 'comment':
            parent = Comment.objects.get(pk=request.data['object_id'])
        else:
            parent = ''
        comment = Comment.objects.create(text=request.data['text'], author=self.request.user, content_object=parent)
        return Response()


class CommentsPost(APIView):

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        comments = post.comments
        return Response(CommentSerializer(comments, many=True).data)