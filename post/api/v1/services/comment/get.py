from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment


class ShowCommentService(ServiceWithResult):
    comment_id = forms.IntegerField(min_value=1)

    custom_validations = ['_comment_presence', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comment
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
                           ObjectDoesNotExist(f'Comment with id={self.cleaned_data.get("comment_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND
