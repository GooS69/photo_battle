from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from post.my_models.post import Post


class DeletePost(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/delete_post.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('post:user_page', args=[self.request.user.id])
        return super().get_success_url()

    def test_func(self):
        return self.request.user == self.get_object().owner
