from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView

from post.forms.custom_user_avatar_form import CustomUserAvatarForm
from post.forms.custom_user_name_form import CustomUserNameForm
from post.forms.new_post_form import NewPostForm
from post.my_models.custom_user import CustomUser


class UserPage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'post/user_page.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newPostForm'] = NewPostForm
        context['updateNameForm'] = CustomUserNameForm
        context['updateAvatarForm'] = CustomUserAvatarForm
        return context
