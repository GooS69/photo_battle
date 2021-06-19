from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models.post import Post
from .models.comment import Comment


class MainPage(ListView):
    queryset = Post.objects.filter(status='v')
    template_name = 'post/index.html'
    context_object_name = 'posts'


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


#class UpdatePost(UpdateView):
#    model = Post
#    fields = ['name', 'img_large']
#    template_name = 'post/update_post.html'
#    success_url = reverse_lazy('post:main_page')


class UserPage(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = 'post/user.html'
    context_object_name = 'user'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(owner_id=self.kwargs['pk'])
        return context
