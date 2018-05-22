from django.contrib import admin

from .models import BlogLike


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
	list_display = ['user', 'blog']
