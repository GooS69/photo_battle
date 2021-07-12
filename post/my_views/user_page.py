from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.html import escape
from django.views.generic import DetailView

from post.my_models.custom_user import CustomUser
from post.my_models.post import Post


class UserPage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = 'post/user_page.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = escape(self.request.GET.get('status', 'None'))
        context['posts'] = Post.objects.filter(owner_id=self.kwargs['pk'], status=status)
        return context
