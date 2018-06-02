#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 11:16


from django.urls import path, include, re_path

from api import views

urlpatterns = [
	path('hotblog/', views.HotBlogListView.as_view(), name='hot_blog'),
	path('blogdetail/', views.BlogDetailAPIView.as_view(), name='blog_detail'),
]
