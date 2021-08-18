from rest_framework import serializers
from rest_framework.fields import IntegerField

from post.my_models.custom_user import CustomUser


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'is_staff']


class UsersRequest(serializers.Serializer):
    page = IntegerField(min_value=1, default=1)
