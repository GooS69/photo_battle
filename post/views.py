from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, Comment, User


def index(request):
    posts = Post.objects.all()
    if not posts:
        return HttpResponse("<H3>No posts</H3>")
    else:
        return render(request, 'post/index.html', context={'posts':posts})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(parent_id=post_id)

    return render(request, 'post/detail.html', context={'post':post, 'comments' : comments})