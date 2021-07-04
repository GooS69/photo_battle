from django.forms import ModelForm, HiddenInput
from ..models.comment import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {'parent_id': HiddenInput,
                   'parent_type': HiddenInput
                   }
