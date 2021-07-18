from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic import ListView

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ProcessFormView, FormMixin

from post.forms.custom_user_avatar_form import CustomUserAvatarForm
from post.forms.custom_user_name_form import CustomUserNameForm
from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


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


class UserPosts(UserPassesTestMixin, ListView):
    template_name = 'post/components/user_posts_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.filter(owner=self.request.user).filter(status=self.kwargs['status'])
        return super().get_queryset()

    def test_func(self):
        return self.request.user.id == self.kwargs['pk']