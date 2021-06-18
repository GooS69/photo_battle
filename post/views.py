from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models.post import Post
from .models.comment import Comment


class MainPage(ListView):
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'


class DetailPage(DetailView):
    model = Post
    template_name = 'post/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['pk'])
        return context


class CreateNewPost(CreateView):
    model = Post
    fields = ['name', 'img_large']
    template_name = 'post/new_post.html'
    success_url = reverse_lazy('post:main_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
