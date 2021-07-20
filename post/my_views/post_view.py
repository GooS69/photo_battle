from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.utils.html import escape
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, ProcessFormView, DeletionMixin

from post.forms.new_post_form import NewPostForm
from post.my_models.post import Post


class CreateNewPost(FormMixin, LoginRequiredMixin, ProcessFormView):
    login_url = '/login/vk-oauth2'
    form_class = NewPostForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return HttpResponse(status=200)


class DeletePost(UserPassesTestMixin, DeletionMixin, SingleObjectMixin,View):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=200)

    def test_func(self):
        return self.request.user == self.get_object().owner


class PostList(ListView):
    template_name = 'post/components/post_list.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_ordering(self):
        return self.kwargs['sorting']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorting'] = self.get_ordering()
        return context

    def get_queryset(self):
        user_filter = escape(self.request.GET['filter'])
        self.queryset = Post.objects.filter(status='verified', name__icontains=user_filter)
        return super().get_queryset()
