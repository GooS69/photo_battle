from rest_framework import serializers
from rest_framework.fields import ChoiceField, CharField, IntegerField

from post.my_models.comment import Comment
from post.my_models.post import Post


class CreateCommentSerializer(serializers.ModelSerializer):
    content_type = ChoiceField(choices=[('post', 'post'), ('comment', 'comment')])

    class Meta:
        model = Comment
        fields = ['text', 'content_type', 'object_id']


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Comment):
            return CommentSerializer(value).data
        else:
            raise Exception('Unexpected type of content_object')


class CommentSerializer(serializers.ModelSerializer):
    comments = ContentObjectRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ['author', 'text', 'comments',]


class PutCommentSerializer(serializers.Serializer):
    text = CharField(min_length=1)


class CommentsRequest(serializers.Serializer):
    post_id = IntegerField(min_value=1)