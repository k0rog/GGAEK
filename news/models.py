from django.db import models
from PIL import Image
from django.conf import settings
import os
from users.models import CustomUser
import re


def get_image_path(self, filename):
    return f"news/{self.title}/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    announce = models.CharField(max_length=200)
    text = models.TextField()
    save_transparency = models.BooleanField()
    date = models.DateField()
    cover = models.ImageField(upload_to=get_image_path)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts')
    dislikes = models.ManyToManyField(CustomUser, related_name='disliked_posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    views = models.ManyToManyField(CustomUser, related_name='viewed_posts')
    slug = models.SlugField(max_length=150)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        images = [self.cover]
        if self.save_transparency:
            images += re.findall('<img alt=\"\" src=\"(.*?)\"', self.text)

        for i, image_path in enumerate(images):
            with Image.open(image_path) as image:
                image = image.resize((800, 800), Image.ANTIALIAS)

                new_path = get_image_path(self, os.path.split(os.path.splitext(str(image_path))[0] + '.jpeg')[-1])

                image = image.convert('RGB')
                image.save(settings.MEDIA_ROOT / new_path, 'JPEG', quality=99)

            os.remove(f'{settings.MEDIA_ROOT}/{image_path}')

            self.text = re.sub(f'{image_path}', new_path, self.text)

        super().save()

        # with Image.open(self.cover) as image:
        #     image = image.resize((800, 800), Image.ANTIALIAS)
        #
        #     new_path = os.path.splitext(str(self.cover))[0] + '.jpeg'
        #
        #     image = image.convert('RGB')
        #     image.save(settings.MEDIA_ROOT / new_path, 'JPEG', quality=99)
        #
        #     self.cover = new_path
        #
        # images = re.findall('<img alt=\"\" src=\"(.*?)\"', self.text)

