#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 15:15


from rest_framework import permissions


class IsOwnerWriteOnly(permissions.BasePermission):
	"""
		只有登录用户才能
	"""

	def has_object_permission(self, request, view, obj):
		"""
		这个是对象范围的权限，通常用于验证对象是否属于提交的用户，用户在修改删除博客时就会生效
		"""
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner.id == request.user.id

	def has_permission(self, request, view):
		"""
		这个是views范围的权限，在提交博客的时候，如果没有登录就会返回False，拒绝提交
		"""
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.is_authenticated
