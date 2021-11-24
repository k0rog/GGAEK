from django.shortcuts import render
from .models import Post


def news(request):
    posts = Post.objects.all()
    return render(request, 'news.html', {'posts': posts})


def post_detail(request, service_slug):
    post = Post.objects.filter(slug__exact=service_slug).first()
    return render(request, 'post.html', {'post': post})
