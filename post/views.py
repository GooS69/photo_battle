from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, View
from django.views.generic.edit import FormMixin, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .forms.comment_form import CommentForm
from django.urls import reverse_lazy
from .models.post import Post
from .models.comment import Comment
from .models.like import Like


class MainPage(ListView):
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_ordering(self):
        self.ordering = self.request.GET.get('sorting', '-number_of_likes')
        return super().get_ordering()

    def get_queryset(self):
        filter = self.request.GET.get('filter', '')
        self.queryset = Post.objects.filter(status='verified').filter(name__icontains=filter)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class DetailPage(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
        context['comments'] = self.get_object().comments.all()
        if self.request.user.is_authenticated:
            context['is_user_like_this'] = Like.objects.filter(user=self.request.user,
                                                               post_id=self.kwargs['pk']).exists()
            context['comment_form'] = CommentForm
        return context


class CreateNewPost(LoginRequiredMixin, CreateView):
    login_url = '/login/vk-oauth2'

    model = Post
    fields = ['name', 'img']
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


class CreateComment(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def get_success_url(self):
        self.success_url = reverse_lazy('post:detail_page', args=[self.kwargs['pk']])
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        if self.request.POST.get('parent'):
            form.instance.parent = Comment.objects.get(id=int(self.request.POST['parent']))
        form.save()
        return super().form_valid(form)


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
