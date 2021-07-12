from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from post.my_models.post import Post


class CreateNewPost(LoginRequiredMixin, CreateView):
    login_url = '/login/vk-oauth2'

    model = Post
    fields = ['name', 'img']
    template_name = 'post/new_post.html'
    success_url = reverse_lazy('post:main_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
