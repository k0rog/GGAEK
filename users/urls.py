from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserLogoutView.as_view(), name='logout'),
]
