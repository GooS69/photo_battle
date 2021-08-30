from django import forms
from django.forms import ModelForm, HiddenInput
from ..my_models.comment import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {'target_id': HiddenInput,
                   'text': forms.Textarea(attrs={'rows': 5, 'cols': 30})
                   }
