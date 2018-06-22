#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-18 0:06


import xadmin
from xadmin import views

from blog.models import Blog, BlogType


class BlogAdmin(object):
	list_display = ['title', 'author', 'blog_type', 'created_time', 'last_update_time']
	list_filter = ['title', 'author', 'blog_type', 'created_time', 'last_update_time']
	search_fields = ['title', 'author', 'blog_type']
	style_fields = {'content': 'ueditor'}


class BlogTypeAdmin(object):
	list_display = ['type_name']
	list_filter = ['type_name']
	search_fields = ['type_name']


xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(BlogType, BlogTypeAdmin)


class GlobalSettings(object):
	site_title = 'BiliBlog的后台管理'
	site_footer = 'FlynnGod的BiliBlog项目Demo'
	menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSettings)
