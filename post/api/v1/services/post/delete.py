from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class PostDeleteService(ServiceWithResult):
    user = ModelField(CustomUser)
    post_id = forms.IntegerField(min_value=1)

    custom_validations = ['_post_presence', ]

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
            self.add_error('post_id', ObjectDoesNotExist(f'Post with id={self.cleaned_data.get("post_id")} not presence'))
            self.response_status = status.HTTP_404_NOT_FOUND
