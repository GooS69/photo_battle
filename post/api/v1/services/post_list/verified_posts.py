from functools import lru_cache

from django import forms

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.post import Post


class VerifiedPostListService(ServiceWithResult):
    filter = forms.CharField(required=False, min_length=3)
    ordering = forms.ChoiceField(choices=[('-number_of_likes', 'number_of_likes'),
                                         ('-number_of_comments', 'number_of_comments'), ('-pub_date', 'pub_date')])

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    def _queryset(self):
        return Post.objects.filter(status='verified', name__icontains=self.cleaned_data.get('filter')).order_by(self.cleaned_data.get('ordering'))
