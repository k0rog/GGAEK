from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('<slug:post_slug>', views.GameDetailView.as_view(), name="news_detail"),
    path('<slug:post_slug>/likes', views.add_like, name='add_like'),
    path('<slug:post_slug>/dislikes', views.add_dislike, name='add_dislike'),
]
