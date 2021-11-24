from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Содержание статьи', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'likes_count', 'dislikes_count', 'view_count', 'get_image']
    readonly_fields = ['get_image']
    prepopulated_fields = {'slug': ('title',)}
    exclude = ['likes', 'dislikes', 'views']

    form = PostAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.cover.url}" width="80" height="60"')

    def likes_count(self, obj):
        return obj.likes.count()

    def dislikes_count(self, obj):
        return obj.dislikes.count()

    def view_count(self, obj):
        return obj.views.count()

    get_image.short_description = "Image"


@admin.register(Category)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

