#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-18 11:34


import xadmin

from read_statistics.models import ReadDetail, ReadNum


class ReadDetailAdmin(object):
	list_display = ['date', 'object_id', 'read_num']
	list_filter = ['date', 'object_id', 'read_num']
	search_fields = ['date', 'object_id']


class ReadNumAdmin(object):
	list_display = ['object_id', 'read_num']
	list_filter = ['object_id']
	search_fields = ['object_id']


xadmin.site.register(ReadDetail, ReadDetailAdmin)
xadmin.site.register(ReadNum, ReadNumAdmin)
