#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-18 0:30


import xadmin

from comment.models import Comment, NewCommentCount


class CommentAdmin(object):
	list_display = ['object_id', 'comment_time', 'user']
	search_fields = ['object_id', 'user']
	list_filter = ['object_id', 'comment_time', 'user']


class NewCommentCountAdmin(object):
	list_display = ['user', 'count']
	search_fields = ['user']
	list_filter = ['user', 'count']


xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(NewCommentCount, NewCommentCountAdmin)
