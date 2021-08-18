from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class UserPostsService(ServiceWithResult):
    user_id = forms.IntegerField(min_value=1)

    custom_validations = ['_user_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    def _queryset(self):
        return Post.objects.filter(owner=self.cleaned_data.get('user_id'))

    @property
    def _user(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data.get('user_id'))
        except ObjectDoesNotExist:
            return None

    def _user_presence(self):
        if not self._user:
            self.add_error('user_id',
                           ObjectDoesNotExist(f'User with id={self.cleaned_data.get("user_id")} not presence'))
            self.response_status = status.HTTP_404_NOT_FOUND
