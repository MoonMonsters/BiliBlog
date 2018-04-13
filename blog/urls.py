#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-04-07 14:54

from django.urls import path
from . import views

urlpatterns = [
	path('', views.blog_list, name='blog_list'),
	# http://localhost:8000/blog/1
	path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
	path('type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
]
