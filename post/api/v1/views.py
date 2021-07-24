from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.v1.my_serializers.comment_serializer import CommentSerializer
from post.api.v1.my_serializers.post_serializer import PostSerializer
from post.my_models.comment import Comment
from post.my_models.post import Post


class PostList(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentList(APIView):

    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)