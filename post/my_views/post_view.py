from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.views import View
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
