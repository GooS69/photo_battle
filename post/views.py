from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Post, Comment, User


def index(request):
    posts = get_list_or_404(Post)
    return render(request, 'post/index.html', context={'posts':posts})


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = get_list_or_404(Comment,parent=post)

    return render(request, 'post/detail.html', context={'post':post, 'comments' : comments})