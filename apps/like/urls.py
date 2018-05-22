#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-22 10:57
from django.urls import path, re_path

from . import views

urlpatterns = [
	path('blog/', views.give_blog_a_like, name='blog_like'),
]
