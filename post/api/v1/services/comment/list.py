from django import forms

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment


class CommentsService(ServiceWithResult):
    post_id = forms.IntegerField(min_value=1, required=False)
    target_id = forms.IntegerField(min_value=1, required=False)
    author_id = forms.IntegerField(min_value=1, required=False)
    text = forms.CharField(min_length=3, required=False)

    def process(self):
        if self.is_valid():
            self.result = self._comments
        return self

    @property
    def _comments(self):
        queryset = Comment.objects.all()
        if self.cleaned_data.get('post_id'):
            queryset = queryset.filter(root_post=self.cleaned_data.get('post_id'))
        if self.cleaned_data.get('target_id'):
            queryset = queryset.filter(object_id=self.cleaned_data.get('target_id'))
        if self.cleaned_data.get('author_id'):
            queryset = queryset.filter(author=self.cleaned_data.get('author_id'))
        return queryset.filter(text__icontains=self.cleaned_data.get('text'))
