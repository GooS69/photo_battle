from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

from post.my_models.comment import Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    target_id = IntegerField(min_value=1)
    root_post_id = IntegerField(min_value=1)

    class Meta:
        model = Comment
        fields = ['root_post_id', 'text', 'target_id']


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


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'root_post', 'author', 'text', 'target']


class PutCommentSerializer(serializers.Serializer):
    text = CharField(min_length=1)


class CommentsRequest(serializers.Serializer):
    post_id = IntegerField(min_value=1, required=False)
    target_id = IntegerField(min_value=1, required=False)
    author_id = IntegerField(min_value=1, required=False)
    text = CharField(min_length=3, required=False)
    page = IntegerField(min_value=1, default=1)
