from django.views.generic import ListView, DetailView
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
        context['comments'] = Comment.objects.filter(post_id=self.kwargs.get(self.pk_url_kwarg))
        return context
