from rest_framework import serializers

from post.api.v1.my_serializers.comment_serializers import CommentSerializer
from post.my_models.comment import Comment
from post.my_models.post import Post


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['name', 'img', ]


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'name', 'img', 'owner', 'pub_date', 'number_of_likes', 'number_of_comments']