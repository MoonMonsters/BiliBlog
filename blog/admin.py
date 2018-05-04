from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
	list_display = ['id', 'type_name']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	list_display = ['title', 'blog_type', 'author', 'read_num', 'created_time', 'last_update_time']
