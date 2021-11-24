from django.urls import path
from . import views


urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('<slug:service_slug>', views.post_detail, name="news_detail")
]
