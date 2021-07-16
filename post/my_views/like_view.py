from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.views import View

from post.my_models.like import Like


class DeleteLike(View, UserPassesTestMixin):
    def test_func(self):
        return Like.objects.filter(user=self.request.user, post_id=self.kwargs['pk']).exists()

    def get(self, request, *args, **kwargs):
        Like.objects.get(user=self.request.user, post_id=self.kwargs['pk']).delete()
        return HttpResponse(status=200)


class CreateLike(View, UserPassesTestMixin):
    def test_func(self):
        return not Like.objects.filter(user=self.request.user, post_id=self.kwargs['pk']).exists()

    def get(self, request, *args, **kwargs):
        Like.objects.create(user=self.request.user, post_id=self.kwargs['pk'])
        return HttpResponse(status=200)
