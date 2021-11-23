from django.db import models


class FeedbackMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    text = models.TextField()
    evaluation = models.IntegerField()
