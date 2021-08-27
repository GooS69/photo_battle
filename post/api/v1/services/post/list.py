from django import forms
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from service_objects.fields import ModelField

from post.api.utils.service_with_result import ServiceWithResult
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class PostsService(ServiceWithResult):
    user = ModelField(CustomUser, required=False)
    filter = forms.CharField(min_length=3, required=False)
    owner_id = forms.IntegerField(min_value=1, required=False)
    status = forms.ChoiceField(
        choices=[('verified', 'verified'), ('not_verified', 'not_verified'), ('rejected', 'rejected')], required=False)
    ordering = forms.ChoiceField(choices=[('-number_of_likes', 'number_of_likes'),
                                          ('-number_of_comments', 'number_of_comments'),
                                          ('-pub_date', 'pub_date')], required=False)

    custom_validations = ['_owner_presence', '_user_permissions']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._queryset
        return self

    @property
    def _queryset(self):
        queryset = Post.objects.all()
        if self.cleaned_data.get('owner_id'):
            queryset = queryset.filter(owner=self.cleaned_data.get('owner_id'))
        if self.cleaned_data.get('status'):
            queryset = queryset.filter(status=self.cleaned_data.get('status'))
        if self.cleaned_data.get('ordering'):
            queryset = queryset.order_by(self.cleaned_data.get('ordering'))
        return queryset.filter(name__icontains=self.cleaned_data.get('filter'))

    @property
    def _owner(self):
        try:
            return CustomUser.objects.get(id=self.cleaned_data.get('owner_id'))
        except ObjectDoesNotExist:
            return None

    def _owner_presence(self):
        if self.cleaned_data.get('owner_id') and not self._owner:
            self.add_error('owner_id',
                           ObjectDoesNotExist(f'User with id={self.cleaned_data.get("owner_id")} not found'))
            self.response_status = status.HTTP_404_NOT_FOUND

    def _user_permissions(self):
        if self.cleaned_data.get('status') in ['not_verified', 'rejected'] or not self.cleaned_data.get('status') \
                and (not self.cleaned_data.get('user')
                     or (self.cleaned_data.get('user').id != self.cleaned_data.get('owner_id')
                         and not self.cleaned_data.get('user').is_staff)):
            self.add_error('user', PermissionDenied(f'User must be owner or admin to see posts with current status'))
            self.response_status = status.HTTP_403_FORBIDDEN
