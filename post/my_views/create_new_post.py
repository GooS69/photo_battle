from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import FormMixin, ProcessFormView

from post.forms.new_post_form import NewPostForm


class CreateNewPost(FormMixin, LoginRequiredMixin, ProcessFormView):
    login_url = '/login/vk-oauth2'
    form_class = NewPostForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return HttpResponse(status=200)
