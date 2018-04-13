#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-04-07 17:46
from django.shortcuts import render_to_response


def home(request):
	context = {}
	return render_to_response('home.html', context)
