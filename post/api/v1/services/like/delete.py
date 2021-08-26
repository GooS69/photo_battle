from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.like import Like
from post.my_models.post import Post


class LikeDeleteService(ServiceWithResult):
    user = ModelField(CustomUser)
    post_id = forms.IntegerField(min_value=1) # expected like id to work with it

    custom_validations = ['_post_presence', '_like_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self._delete_like()
        return self

    def _delete_like(self):
        self._like.delete()

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data.get('post_id'))
        except ObjectDoesNotExist:
            return None

    @property
    @lru_cache()
    def _like(self):
        if self._post:
            try:
                return Like.objects.get(user=self.cleaned_data.get('user'), post=self._post)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Post with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _like_presence(self):
        if self._post and not self._like:
            self.add_error(None, ObjectDoesNotExist(f'Like for post with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND
