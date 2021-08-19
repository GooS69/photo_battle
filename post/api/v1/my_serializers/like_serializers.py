from rest_framework import serializers
from rest_framework.fields import IntegerField


class LikeSerializer(serializers.Serializer):
    post_id = IntegerField(min_value=1)
