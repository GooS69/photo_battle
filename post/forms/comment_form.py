from django.forms import ModelForm
from ..models.comment import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
