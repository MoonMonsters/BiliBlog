#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-18 0:50


import xadmin

from like.models import BlogLike


class BlogLikeAdmin(object):
	list_display = ['user', 'blog']


xadmin.site.register(BlogLike, BlogLikeAdmin)
