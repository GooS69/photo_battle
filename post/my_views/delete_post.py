from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin

from post.my_models.post import Post


class DeletePost(UserPassesTestMixin, DeletionMixin, SingleObjectMixin,View):
    model = Post

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=200)

    def test_func(self):
        return self.request.user == self.get_object().owner
