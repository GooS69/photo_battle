from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from post.forms.comment_form import CommentForm
from post.my_models.like import Like
from post.my_models.post import Post


class DetailPage(UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.status == 'verified'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_user_like_this'] = Like.objects.filter(user=self.request.user,
                                                               post_id=self.kwargs['pk']).exists()
            context['comment_form'] = CommentForm
        return context
