from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .models import Post, Comment


def index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html', context={'posts': posts})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(parent_id=post_id)

    return render(request, 'post/detail.html', context={'post': post, 'comments': comments})


def auth_logout(request):
    logout(request)
    return redirect('post:index')