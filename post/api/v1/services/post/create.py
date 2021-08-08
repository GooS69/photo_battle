from django import forms
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class PostCreateService(ServiceWithResult):
    user = ModelField(CustomUser)
    name = forms.CharField()

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self):
        return Post.objects.create(owner=self.cleaned_data.get("user"),
                                   name=self.cleaned_data.get('name'),
                                   img=self.files.get('img'))
