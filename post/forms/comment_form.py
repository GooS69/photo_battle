from django.forms import ModelForm, HiddenInput
from ..my_models.comment import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {'parent_id': HiddenInput,
                   'parent_type': HiddenInput
                   }
