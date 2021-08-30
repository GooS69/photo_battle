from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.comment import Comment
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post
from post.my_models.target_base_class import TargetBaseClass


class CreateCommentService(ServiceWithResult):
    root_post_id = forms.IntegerField(min_value=1)
    text = forms.CharField()
    user = ModelField(CustomUser)
    target_id = forms.IntegerField(min_value=1)

    custom_validations = ['_target_presence', '_root_post_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_comment()
        return self

    def _create_comment(self):
        return Comment.objects.create(root_post=self._root_post,
                                      text=self.cleaned_data.get('text'),
                                      author=self.cleaned_data.get('user'),
                                      target=self._target)

    @property
    @lru_cache()
    def _target(self):
        try:
            return TargetBaseClass.objects.get(id=self.cleaned_data.get('target_id'))
        except ObjectDoesNotExist:
            return None

    @property
    @lru_cache()
    def _root_post(self):
        try:
            return Post.objects.get(id=self.cleaned_data.get('root_post_id'), status='verified')
        except ObjectDoesNotExist:
            return None

    def _target_presence(self):
        if not self._target:
            self.add_error(None, ObjectDoesNotExist(f'Target object with id='
                                                    f'{self.cleaned_data.get("target_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _root_post_presence(self):
        if not self._root_post:
            self.add_error('root_post_id', ObjectDoesNotExist(f'Verified post with id='
                                                              f'{self.cleaned_data.get("root_post_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND
