from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.like import Like


class LikeDeleteService(ServiceWithResult):
    user = ModelField(CustomUser)
    like_id = forms.IntegerField(min_value=1)

    custom_validations = ['_like_presence', '_user_permissions']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._delete_like()
        return self

    def _delete_like(self):
        self._like.delete()

    @property
    @lru_cache()
    def _like(self):
        try:
            return Like.objects.get(id=self.cleaned_data.get('like_id'))
        except ObjectDoesNotExist:
            return None

    def _like_presence(self):
        if not self._like:
            self.add_error('like_id', ObjectDoesNotExist(f'Like with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _user_permissions(self):
        if self._like and \
                not (self.cleaned_data.get('user') == self._like.user or self.cleaned_data.get('user').is_staff):
            self.add_error('user', PermissionDenied(f'User must be owner or admin'))
            self.response_status = status.HTTP_403_FORBIDDEN
