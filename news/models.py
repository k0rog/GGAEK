from django.db import models
from PIL import Image
from django.conf import settings
import os
from users.models import CustomUser
import re
import shutil


def get_image_path(self, filename):
    return f"news/{self.title}/{filename}"


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Ip(models.Model):
    ip = models.CharField(max_length=150)


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
    views = models.ManyToManyField(Ip, related_name='viewed_posts')
    slug = models.SlugField(max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_title = self.title

    def __str__(self):
        return self.title

    def move_image_to_post_folder(self, image_path, convert_jpeg=True):
        with Image.open(image_path) as image:
            image = image.resize((800, 800), Image.ANTIALIAS)

            filename = os.path.basename(image_path)
            if convert_jpeg:
                new_filename = os.path.splitext(filename)[0] + '.jpeg'

                new_path = get_image_path(self, new_filename)

                image = image.convert('RGB')
                image.save(settings.MEDIA_ROOT / new_path, 'JPEG', quality=70)
            else:
                new_path = get_image_path(self, filename)
                image.save(settings.MEDIA_ROOT / new_path)

        return new_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.title != self.previous_title and \
                not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'news', self.title)):
            os.mkdir(os.path.join(settings.MEDIA_ROOT, 'news', self.title))

        self.cover = self.move_image_to_post_folder(os.path.join(settings.MEDIA_ROOT, str(self.cover)))

        text_images = re.findall('<img alt=\"\" src=\"(.*?)\"', self.text)
        for image_path in text_images:
            new_path = self.move_image_to_post_folder(f'{settings.BASE_DIR}{image_path}', self.save_transparency)

            self.text = re.sub(f'{image_path}', f'/media/{new_path}', self.text)

        current_images = [str(self.cover)] + [re.sub('/media/', '', image)
                                              for image
                                              in re.findall('<img alt=\"\" src=\"(.*?)\"', self.text)]
        for file in os.listdir(os.path.join(settings.MEDIA_ROOT, 'news', self.title)):
            file = get_image_path(self, file)
            if file not in current_images:
                os.remove(os.path.join(settings.MEDIA_ROOT, file))

        if os.path.exists(settings.MEDIA_ROOT / 'uploads'):
            shutil.rmtree(settings.MEDIA_ROOT / 'uploads')

        if self.title != self.previous_title and self.previous_title != '' and \
                os.path.exists(os.path.join(settings.MEDIA_ROOT, 'news', self.previous_title)):
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'news', self.previous_title))

        super().save(*args, **kwargs)
