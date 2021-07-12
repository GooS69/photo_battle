from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from post.forms.custom_user_form import CustomUserForm
from post.my_models.custom_user import CustomUser


class UpdateUser(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'post/update_user.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('post:user_page', args=[self.kwargs['pk']])
        return super().get_success_url()

    def test_func(self):
        return self.request.user == self.get_object()
