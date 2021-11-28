from .models import Post, Category, Ip
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django import http

class NewsListView(ListView):
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 30
    paginate_orphans = 9

    def get_queryset(self):
        category = self.request.GET.get('category', None)

        news = Post.objects.all() if category is None else Post.objects.filter(category__title=category)

        return news

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()

        categories = Category.objects.all()
        context_data['categories'] = categories

        return context_data


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class GameDetailView(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])

        user_ip = get_user_ip(self.request)

        ip, _ = Ip.objects.get_or_create(ip=user_ip)

        post.views.add(ip.id)

        return post


def add_like(request, post_slug):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return http.HttpResponseNotAllowed('')

        post = Post.objects.filter(slug=post_slug).first()
        post.likes.add(request.user)

        return http.HttpResponse(post.likes.count())

    return http.Http404('')


def add_dislike(request, post_slug):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return http.HttpResponseNotAllowed('')

        post = Post.objects.filter(slug=post_slug).first()
        post.dislikes.add(request.user)

        return http.HttpResponse(post.dislikes.count())

    return http.Http404('')
