#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-23 0:19


import xadmin
from .models import IPSaver


class IPSaverAdmin(object):
	list_display = ['ip', 'blog_id', 'visited_time']
	search_fields = ['ip', 'blog_id']
	list_filter = ['ip', 'blog_id']


xadmin.site.register(IPSaver, IPSaverAdmin)
