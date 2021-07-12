from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, FormView

from post.forms.comment_form import CommentForm
from post.my_models.comment import Comment
from post.my_models.like import Like
from post.my_models.post import Post


class DetailPage(View):

    @staticmethod
    def get(request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    @staticmethod
    def post(request, *args, **kwargs):
        view = CreateComment.as_view()
        return view(request, *args, **kwargs)


class PostDisplay(UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.status == 'verified'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['comments'] = self.get_object().comments.all()
        if self.request.user.is_authenticated:
            context['is_user_like_this'] = Like.objects.filter(user=self.request.user,
                                                               post_id=self.kwargs['pk']).exists()
            context['comment_form'] = CommentForm
        return context


class CreateComment(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def get_success_url(self):
        self.success_url = reverse_lazy('post:detail_page', args=[self.kwargs['pk']])
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        if self.request.POST.get('parent_type') == 'post':
            form.instance.content_object = Post.objects.get(pk=self.request.POST.get('parent_id'))
        elif self.request.POST.get('parent_type') == 'comment':
            form.instance.content_object = Comment.objects.get(pk=self.request.POST.get('parent_id'))

        form.save()
        return super().form_valid(form)
