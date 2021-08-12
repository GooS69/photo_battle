from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.post import Post


class PutPostService(ServiceWithResult):
    post_id = forms.IntegerField(min_value=1)
    name = forms.CharField(min_length=1)

    custom_validations = ['_is_user_owner_or_admin', '_post_presence', '_img_presence', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._put()
        return self

    def _put(self):
        post = self._post
        post.name = self.cleaned_data.get('name')
        post.img = self.files.get('img')
        post.status = 'not_verified'
        post.save()

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.filter(status='verified').get(id=self.cleaned_data.get('post_id'))
        except ObjectDoesNotExist:
            return None

    def _is_user_owner_or_admin(self):
        if self._post:
            if self._post.owner != self.cleaned_data.get('user') and not self.cleaned_data.get('user').is_staff:
                self.add_error('user', PermissionDenied(f'Forbidden'))
                self.response_status = status.HTTP_403_FORBIDDEN


    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Verified post with id={self.cleaned_data.get("post_id")} not presence'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _img_presence(self):
        if not self.files.get('img'):
            self.add_error(None, ObjectDoesNotExist(f'Image not presence'))
            self.response_status = status.HTTP_400_BAD_REQUEST
