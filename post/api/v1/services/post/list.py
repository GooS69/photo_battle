from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class PostsService(ServiceWithResult):
    user = ModelField(CustomUser, required=False)
    preset = forms.ChoiceField(choices=[('user_page', 'user_page'), ('main_page', 'main_page')], required=True)
    filter = forms.CharField(min_length=3, required=False)
    ordering = forms.ChoiceField(choices=[('-number_of_likes', 'number_of_likes'),
                                          ('-number_of_comments', 'number_of_comments'),
                                          ('-pub_date', 'pub_date')],required=False)
    status = forms.ChoiceField(
        choices=[('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')], required=False)

    custom_validations = ['_user_page_preset_validate',]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    def _queryset(self):
        if self.cleaned_data.get('preset') == 'user_page':
            return self._user_page_preset()
        elif self.cleaned_data.get('preset') == 'main_page':
            return self._main_page_preset()

    def _user_page_preset(self):
        if self.cleaned_data.get('status'):
            return Post.objects.filter(owner=self.cleaned_data.get('user'), status=self.cleaned_data.get('status'))
        else:
            return Post.objects.filter(owner=self.cleaned_data.get('user'))

    def _main_page_preset(self):
        queryset = Post.objects.filter(status='verified')
        if self.cleaned_data.get('filter'):
            queryset = queryset.filter(name__icontains=self.cleaned_data.get('filter'))
        if self.cleaned_data.get('ordering'):
            queryset = queryset.order_by(self.cleaned_data.get('ordering'))
        return queryset

    def _user_page_preset_validate(self):
        if self.cleaned_data.get('preset') == 'user_page':
            if not self.cleaned_data.get('user'):
                self.add_error('user', ObjectDoesNotExist('User not presence'))
                self.response_status = status.HTTP_404_NOT_FOUND

