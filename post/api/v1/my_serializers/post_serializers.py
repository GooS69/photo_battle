from rest_framework import serializers

from post.my_models.post import Post
from rest_framework.fields import CharField, ChoiceField, IntegerField, ImageField


class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['name', 'img', ]


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'name', 'img', 'status', 'owner', 'pub_date', 'number_of_likes', 'number_of_comments']


class ParticleUpdatePostSerializer(serializers.Serializer):
    id = IntegerField(min_value=1)
    name = CharField(min_length=1, required=False)
    img = ImageField(required=False)
    status = ChoiceField([('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')],
                         required=False)


class PostsRequest(serializers.Serializer):
    filter = CharField(min_length=3, required=False)
    owner_id = IntegerField(min_value=1, required=False)
    status = ChoiceField([('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')],
                         required=False)
    ordering = ChoiceField([('-number_of_likes', 'likes'),
                            ('-number_of_comments', 'comments'), ('-pub_date', 'pub_date')], required=False)
    page = IntegerField(min_value=1, default=1)


class ChangePostStatusRequest(serializers.Serializer):
    status = ChoiceField(choices=[('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')])
