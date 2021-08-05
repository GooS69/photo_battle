from django import forms
from django.core.exceptions import ObjectDoesNotExist
from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.post import Post


class PostShowService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    custom_validations = ['_post_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._post
        return self

    @property
    def _post(self):
        try:
            return Post.objects.get(id=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            return None

    def _post_presence(self):
        if not self._post:
            self.add_error('id', ObjectDoesNotExist(f"Post with id={self.cleaned_data['id']} not found"))
