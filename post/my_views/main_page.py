from django.views.generic import ListView
from django.utils.html import escape
from ..my_models.post import Post


class MainPage(ListView):
    template_name = 'post/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_ordering(self):
        self.ordering = escape(self.request.GET.get('sorting', '-number_of_likes'))
        return super().get_ordering()

    def get_queryset(self):
        name_filter = escape(self.request.GET.get('filter', ''))
        self.queryset = Post.objects.filter(status='verified').filter(name__icontains=name_filter)
        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context
