from functools import lru_cache

from django import forms

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.post import Post


class VerifiedPostListService(ServiceWithResult):
    filter = forms.CharField(min_length=0, strip=False)

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    @lru_cache()
    def _queryset(self):
        return Post.objects.filter(status='verified', name__icontains=self.cleaned_data.get('filter'))
