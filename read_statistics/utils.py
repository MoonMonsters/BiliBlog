#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-05 21:11
from django.contrib.contenttypes.models import ContentType

from .models import ReadNum


def read_statistics_once_read(request, obj):
	# obj是传入的实例对象
	ct = ContentType.objects.get_for_model(obj)
	# 构建cookie的key值
	key = '%s_%s_read' % (ct.model, obj.pk)

	# 如果该key值cookie中不存在
	if not request.COOKIES.get(key):
		# 判断ReadNum对象是否存在，如果存在则直接读取ReadNum对象
		if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
			readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
		else:
			# 不存在则创建
			readnum = ReadNum(content_type=ct, object_id=obj.pk)
		# 这个值默认是0，则+1
		readnum.read_num += 1
		# 保存
		readnum.save()
	# 返回应该存入cookie的key值
	return key
