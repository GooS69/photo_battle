from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment
from post.my_models.custom_user import CustomUser


class PutCommentService(ServiceWithResult):
    user = ModelField(CustomUser)
    comment_id = forms.IntegerField(min_value=1)
    text = forms.CharField(min_length=1)

    custom_validations = ['_comment_presence', '_is_user_admin', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._update_comment()
            self.result = self._comment
        return self

    def _update_comment(self):
        self._comment.text = self.cleaned_data.get('text')
        self._comment.save()

    @property
    @lru_cache()
    def _comment(self):
        try:
            return Comment.objects.get(id=self.cleaned_data.get('comment_id'))
        except ObjectDoesNotExist:
            return None

    def _comment_presence(self):
        if not self._comment:
            self.add_error('comment_id',
                           ObjectDoesNotExist(f'Comment with id={self.cleaned_data.get("comment_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _is_user_admin(self):
        if self._comment and not self.cleaned_data.get('user').is_staff:
            self.add_error('user', PermissionDenied(f'Forbidden'))
            self.response_status = status.HTTP_403_FORBIDDEN
