from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.like import Like
from post.my_models.post import Post


class LikeCreateService(ServiceWithResult):
    user = ModelField(CustomUser)
    post_id = forms.IntegerField(min_value=1)

    custom_validations = ['_post_presence', '_like_not_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._new_like
        return self

    @property
    def _new_like(self):
        return Like.objects.create(post=self._post, user=self.cleaned_data.get('user'))

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data.get('post_id'), status='verified')
        except ObjectDoesNotExist:
            return None

    @property
    def _like(self):
        if self._post:
            try:
                return self._post.likes.objects.get(user=self.cleaned_data.get('user'))
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Post with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _like_not_presence(self):
        if self._like:
            self.add_error(None, BadRequest(f'Like for post with id={self.cleaned_data.get("post_id")} already presence'))
            self.response_status = status.HTTP_400_BAD_REQUEST
