from rest_framework import serializers
from rest_framework.fields import IntegerField


class CreateLikeSerializer(serializers.Serializer):
    post_id = IntegerField(min_value=1)


class LikeSerializer(serializers.Serializer):
    like_id = IntegerField(min_value=1)
