from rest_framework import serializers

from post.api.v1.my_serializers.comment_serializer import CommentSerializer
from post.my_models.comment import Comment
from post.my_models.post import Post


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(Comment.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['id', 'img', 'name', 'pub_date', 'owner', 'comments', 'number_of_likes', 'number_of_comments', 'status']