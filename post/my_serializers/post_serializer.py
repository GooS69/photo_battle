from rest_framework import serializers

from post.my_models.post import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'img', 'name', 'pub_date', 'owner', 'comments', 'number_of_likes', 'number_of_comments', 'status']