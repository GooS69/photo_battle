from functools import lru_cache

from django import forms
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class UserPostListService(ServiceWithResult):
    user = ModelField(CustomUser)
    status = forms.ChoiceField(choices=[('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')])

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    @lru_cache()
    def _queryset(self):
        return Post.objects.filter(owner=self.cleaned_data.get('user'), status=self.cleaned_data.get('status'))
