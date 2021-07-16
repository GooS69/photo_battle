from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, JsonResponse

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ProcessFormView, FormMixin

from post.forms.custom_user_avatar_form import CustomUserAvatarForm
from post.forms.custom_user_name_form import CustomUserNameForm
from post.my_models.custom_user import CustomUser


class UpdateUserName(UserPassesTestMixin, SingleObjectMixin, FormMixin, ProcessFormView):
    model = CustomUser
    form_class = CustomUserNameForm

    def form_valid(self, form):
        object = self.get_object()
        object.first_name = form.cleaned_data['first_name']
        object.save()
        return JsonResponse({'first_name': str(object.first_name)})

    def test_func(self):
        return self.request.user == self.get_object()


class UpdateUserAvatar(UserPassesTestMixin, SingleObjectMixin, FormMixin, ProcessFormView):
    model = CustomUser
    form_class = CustomUserAvatarForm

    def form_valid(self, form):
        object = self.get_object()
        object.avatar = form.cleaned_data['avatar']
        object.save()
        return JsonResponse({'avatar': str(object.avatar.url)})

    def test_func(self):
        return self.request.user == self.get_object()
