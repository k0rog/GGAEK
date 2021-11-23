from django.shortcuts import render
from .models import Post


def news(request):
    posts = Post.objects.all()
    return render(request, 'news.html', {'posts': posts})
