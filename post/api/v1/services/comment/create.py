from functools import lru_cache

from django import forms
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class CommentCreateService(ServiceWithResult):
    text = forms.CharField()
    user = ModelField(CustomUser)
    content_type = forms.ChoiceField(choices=[('post', 'post'), ('comment', 'comment')])
    object_id = forms.IntegerField(min_value=1)

    custom_validations = ['_content_type_valid', '_target_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment()
        return self

    def _create_comment(self):
        return Comment.objects.create(text=self.cleaned_data.get('text'),
                                      author=self.cleaned_data.get('user'),
                                      content_object=self._target)

    @property
    @lru_cache()
    def _target(self):
        if self.cleaned_data.get('content_type') == "post":
            try:
                return Post.objects.get(id=self.cleaned_data.get('object_id'))
            except ObjectDoesNotExist:
                return None
        elif self.cleaned_data.get('content_type') == "comment":
            try:
                return Comment.objects.get(id=self.cleaned_data.get('object_id'))
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def _content_type_valid(self):
        if self.cleaned_data.get('content_type') not in ['post', 'comment']:
            self.add_error('content_type', BadRequest('Content_type must be "Post" or "Comment"'))
            self.response_status = status.HTTP_400_BAD_REQUEST

    def _target_presence(self):
        if not self._target:
            self.add_error(None, ObjectDoesNotExist(f'Object {self.cleaned_data.get("content_type")} '
                                                    f'with id={self.cleaned_data.get("object_id")} not presence'))