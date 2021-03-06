from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.post import Post


class ShowPostService(ServiceWithResult):
    post_id = forms.IntegerField(min_value=1)

    custom_validations = ['_post_presence', ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._post
        return self

    @property
    @lru_cache()
    def _post(self):
        try:
            return Post.objects.filter(status='verified').get(id=self.cleaned_data.get('post_id'))
        except ObjectDoesNotExist:
            return None

    def _post_presence(self):
        if not self._post:
            self.add_error('post_id', ObjectDoesNotExist(f'Verified post with id='
                                                         f'{self.cleaned_data.get("post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND
