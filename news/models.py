from django.db import models
from PIL import Image
from django.conf import settings
import os
from users.models import CustomUser


def get_image_path(self, filename):
    return f"news/img/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to=get_image_path)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts')
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image) as image:
            image = image.resize((800, 800), Image.ANTIALIAS)

            new_path = os.path.splitext(str(self.image))[0] + '.jpeg'

            image = image.convert('RGB')
            image.save(settings.MEDIA_ROOT / new_path, 'JPEG', quality=99)

            self.image = new_path
            super().save()
