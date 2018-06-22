#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 11:16


from django.urls import path, include, re_path

from api import views

urlpatterns = [
	path('hotblog/', views.HotBlogListView.as_view(), name='hot_blog'),
	path('blogdetail/', views.BlogDetailAPIView.as_view(), name='blog_detail'),
	path('newcommentcount/', views.NewCommentCountAPIView.as_view(), name='new_comment_count'),
	path('newcommentlist/', views.NewCommentListApiView.as_view(), name='new_comment_list'),
	path('newcommentlist/json/', views.NewCommentListApiView.as_view()),
	path('ipsavernumbers/', views.IPSaverNumbersAPIView.as_view(), name='ip_saver_numbers'),
	path('ipsaverall/', views.IPSaverAllAPIView.as_view(), name='ip_saver_all')
]
