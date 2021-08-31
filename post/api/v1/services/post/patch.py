from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class ParticleUpdatePostService(ServiceWithResult):
    user = ModelField(CustomUser)
    post_id = forms.IntegerField(min_value=1)
    name = forms.CharField(min_length=1, required=False)
    status = forms.ChoiceField(
        choices=[('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')],
        required=False)

    custom_validations = ['_user_permissions', '_post_presence', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._particle_update_post()
        return self

    def _particle_update_post(self):
        post = self._post
        if self.cleaned_data.get('name'):
            post.name = self.cleaned_data.get('name')
        if self.files.get('img'):
            post.img = self.files.get('img')
        if self.cleaned_data.get('status'):
            post.status = self.cleaned_data.get('status')
        else:
            self._post.status = 'not_verified'
        post.save()
        return post

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data.get('post_id'))
        except ObjectDoesNotExist:
            return None

    def _user_permissions(self):
        if self._post and self.cleaned_data.get('status') and not self.cleaned_data.get('user').is_staff:
            self.add_error('user', PermissionDenied(f'Forbidden'))
            self.response_status = status.HTTP_403_FORBIDDEN

    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Post with id={self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND
