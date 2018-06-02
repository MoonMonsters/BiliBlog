#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 11:11

from rest_framework import serializers

from blog.models import Blog


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
