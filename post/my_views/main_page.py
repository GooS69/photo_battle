from django.views.generic import ListView

from ..my_models.like import Like
from ..my_models.post import Post


class MainPage(ListView):
    template_name = 'post/index.html'
    context_object_name = 'posts'
    ordering = '-number_of_likes'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.filter(status='verified')
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorting'] = self.get_ordering()

        if self.request.user.is_authenticated:
            print('hghg')
            context['liked_posts'] = Post.objects.filter(like__user=self.request.user)
        return context
