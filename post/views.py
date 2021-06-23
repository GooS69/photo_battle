from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models.post import Post
from .models.comment import Comment
from .models.like import Like


class MainPage(ListView):
    queryset = Post.objects.filter(status='v')
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 2


class DetailPage(UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.status == 'v'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk'])
        context['is_user_like_this'] = Like.objects.filter(user=self.request.user, post_id=self.kwargs['pk']).exists()
        return context


class CreateNewPost(LoginRequiredMixin, CreateView):
    login_url = '/login/vk-oauth2'

    model = Post
    fields = ['name', 'img_large']
    template_name = 'post/new_post.html'
    success_url = reverse_lazy('post:main_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeletePost(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/delete_post.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('post:user_page', args=[self.request.user.id])
        return super().get_success_url()

    def test_func(self):
        return self.request.user == self.get_object().owner


# temp
class CreateLike(UserPassesTestMixin, RedirectView):
    def test_func(self):
        return not Like.objects.filter(user=self.request.user, post_id=self.kwargs['pk']).exists()

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('post:detail_page', args=[self.kwargs['pk']])
        return super().get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        Like.objects.create(user=self.request.user, post_id=self.kwargs['pk'])
        return super().get(request, *args, **kwargs)


# temp
class DeleteLike(UserPassesTestMixin, RedirectView):
    def test_func(self):
        return Like.objects.filter(user=self.request.user, post_id=self.kwargs['pk']).exists()

    def get_redirect_url(self, *args, **kwargs):
        self.url = reverse_lazy('post:detail_page', args=[self.kwargs['pk']])
        return super().get_redirect_url(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        Like.objects.get(user=self.request.user, post_id=self.kwargs['pk']).delete()
        return super().get(request, *args, **kwargs)


class UserPage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'post/user_page.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(owner_id=self.kwargs['pk'])
        return context


class UpdateUser(UserPassesTestMixin, UpdateView):
    model = User
    fields = ['first_name']
    template_name = 'post/update_user.html'

    def get_success_url(self):
        self.success_url = reverse_lazy('post:user_page', args=[self.kwargs['pk']])
        return super().get_success_url()

    def test_func(self):
        return self.request.user == self.get_object()
