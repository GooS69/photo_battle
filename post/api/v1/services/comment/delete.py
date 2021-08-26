from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment
from post.my_models.custom_user import CustomUser


class DeleteCommentService(ServiceWithResult):
    user = ModelField(CustomUser)
    comment_id = forms.IntegerField(min_value=1)

    custom_validations = ['_comment_presence', '_is_user_owner_or_admin', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._comment.delete()
        return self

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
                           ObjectDoesNotExist(f'Comment with id={self.cleaned_data.get("comment_id")} not presence'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _is_user_owner_or_admin(self):
        if (self._comment and
                (not self._comment.author == self.cleaned_data.get('user') or
                 self.cleaned_data.get('user').is_staff)):
            self.add_error('user', PermissionDenied(f'Forbidden'))
            self.response_status = status.HTTP_403_FORBIDDEN
