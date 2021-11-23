from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Post


@admin.register(Post)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'date', 'get_image']
    readonly_fields = ['get_image']

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="80" height="60"')

    get_image.short_description = "Image"
