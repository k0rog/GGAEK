from . import views
from django.urls import path


urlpatterns = [
    path('', views.FeedbackView.as_view(), name='feedback')
]
