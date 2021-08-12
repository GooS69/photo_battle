from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class CreatePostService(ServiceWithResult):
    user = ModelField(CustomUser)
    name = forms.CharField()

    custom_validations = ['_img_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_post()
        return self

    def _create_post(self):
        return Post.objects.create(owner=self.cleaned_data.get("user"),
                                   name=self.cleaned_data.get('name'),
                                   img=self.files.get('img'))

    def _img_presence(self):
        if not self.files.get('img'):
            self.add_error(None, ObjectDoesNotExist(f'Image not presence'))
            self.response_status = status.HTTP_400_BAD_REQUEST
