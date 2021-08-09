from rest_framework import serializers

from post.my_models.post import Post
from rest_framework.fields import CharField, ChoiceField


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['name', 'img', ]


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'name', 'img', 'owner', 'pub_date', 'number_of_likes', 'number_of_comments']


class PostListRequest(serializers.Serializer):
    filter = CharField(default='')
    ordering = ChoiceField([('-number_of_likes', 'likes'),
                           ('-number_of_comments', 'comments'), ('-pub_date', 'pub_date')])


class UserPostListRequest(serializers.Serializer):
    status = ChoiceField([('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')])
