from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class DeletePostService(ServiceWithResult):
    user = ModelField(CustomUser)
    post_id = forms.IntegerField(min_value=1)

    custom_validations = ['_is_user_owner_or_admin', '_post_presence', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._delete_post()
        return self

    def _delete_post(self):
        self._post.delete()

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data.get('post_id'))
        except ObjectDoesNotExist:
            return None

    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Post with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _is_user_owner_or_admin(self):
        if self._post:
            if self._post.owner != self.cleaned_data.get('user') and not self.cleaned_data.get('user').is_staff:
                self.add_error('user', PermissionDenied(f'Forbidden'))
                self.response_status = status.HTTP_403_FORBIDDEN
