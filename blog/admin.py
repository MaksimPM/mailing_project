from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published', 'views_count')
    list_filter = ('created_at',)
