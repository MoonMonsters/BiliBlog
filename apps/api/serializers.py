#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 11:11
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from blog.models import Blog
from comment.models import Comment


class BlogSerializer(serializers.ModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')
	blog_type = serializers.ReadOnlyField(source='blog_type.type_name')
	# 用来从函数中获取变量，可以在函数中操作变量值然后返回
	read_num = serializers.SerializerMethodField(source='get_read_num')
	last_update_time = serializers.SerializerMethodField(source='get_last_update_time')

	class Meta:
		model = Blog
		fields = ('pk', 'title', 'content', 'author', 'blog_type', 'last_update_time', 'read_num')

	def get_read_num(self, obj):
		"""
		获取博客的总阅读数
		:param obj: Blog对象
		:return: get_read_num是定义在Blog中，用来获取实际阅读量的函数
		"""
		return obj.get_read_num()

	def get_last_update_time(self, obj):
		"""
		格式化时间
		"""
		import datetime
		return datetime.datetime.strftime(obj.last_update_time, '%Y-%m-%d %H:%M')


class NewCommentListSerializer(serializers.ModelSerializer):
	comment_user = serializers.SerializerMethodField(source='get_comment_user')
	blog_title = serializers.SerializerMethodField(source='get_blog_title')
	comment_content = serializers.SerializerMethodField(source='get_comment_content')
	blog_id = serializers.ReadOnlyField(source='object_id')
	comment_time = serializers.SerializerMethodField(source='get_comment_time')

	class Meta:
		model = Comment
		fields = ['blog_id', 'comment_user', 'comment_time', 'blog_title', 'comment_content']

	def get_comment_user(self, obj):
		print('obj = ', obj)
		return obj.user.username

	def get_blog_title(self, obj):
		return Blog.objects.get(id=obj.object_id).title

	def get_comment_content(self, obj):
		return obj.text

	def get_comment_time(self, obj):
		"""
		格式化时间
		"""
		import datetime
		return datetime.datetime.strftime(obj.comment_time, '%Y-%m-%d %H:%M')
