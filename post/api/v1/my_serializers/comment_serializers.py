from rest_framework import serializers


from post.my_models.comment import Comment
from post.my_models.post import Post


class CreateCommentSerializer(serializers.RelatedField):
    class Meta:
        model = Comment
        fields = ['text']


class ContentObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Comment):
            return CommentSerializer(value).data
        elif isinstance(value, Post):
            return 'Post '+ value.pk
        else:
            raise Exception('Unexpected type of content_object')


class CommentSerializer(serializers.ModelSerializer):
    #content_object = ContentObjectRelatedField(many=True, queryset=Comment.objects.all())
    comments = ContentObjectRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ['author', 'text', 'comments',]
