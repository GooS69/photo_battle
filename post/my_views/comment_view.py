from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin

from post.forms.comment_form import CommentForm
from post.my_models.post import Post
from post.my_models.target_base_class import TargetBaseClass


class CreateComment(LoginRequiredMixin, FormMixin, View):
    form_class = CommentForm

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.root_post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.target = TargetBaseClass.objects.get(id=self.request.POST.get('target_id'))

        form.save()
        return HttpResponse(status=200)


class PostComments(TemplateView):
    template_name = 'post/components/comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = Post.objects.get(pk=self.kwargs['pk'])
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        context['comment_form'] = CommentForm
        return context
