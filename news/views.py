from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView


class NewsListView(ListView):
    context_object_name = 'news'
    template_name = 'news.html'
    paginate_by = 30
    # paginate_orphans = 15

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data()

        categories = Category.objects.all()
        context_data['categories'] = categories

        return context_data

# def news(request):
#     posts = Post.objects.all()
#     categories = Category.objects.all()
#
#     return render(request, 'news.html', {'posts': posts, 'categories': categories})


def post_detail(request, service_slug):
    post = Post.objects.filter(slug__exact=service_slug).first()
    return render(request, 'post.html', {'post': post})
