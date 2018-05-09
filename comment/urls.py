#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-09 22:39

from django.urls import path
from . import views

urlpatterns = [
	path('update_comment', views.update_comment, name='update_comment'),
]
