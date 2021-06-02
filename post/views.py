from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post


def index(request):
    return HttpResponse("Hello, world")


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post/detail.html', context={'post':post})