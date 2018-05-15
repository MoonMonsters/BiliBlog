#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-04-07 17:46
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, \
	get_7_days_hot_blogs, get_30_days_hot_blogs
from blog.models import Blog
from .forms import LoginForm, RegisterForm


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	# 得到每天中每天博客的阅读量以及对应的时间
	read_nums, dates = get_seven_days_read_data(blog_content_type)

	context = {}
	# 传到html中
	context['read_nums'] = read_nums
	context['dates'] = dates
	context['today_hot_data'], context['yesterday_hot_data'], context['seven_days_hot_data'], context[
		'thirty_days_hot_data'] = \
		get_datas_from_cache(blog_content_type)
	return render(request, 'home.html', context)


def login(request):
	"""
	登录功能

	# 从request中获得username和password
	username = request.POST.get('username', None)
	password = request.POST.get('password', None)
	# 获取之前的页面，如果没有，则返回到首页
	# 通过reverse方法解析home链接
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	# 使用auth模块进行username和password验证
	user = auth.authenticate(request, username=username, password=password)
	# 如果登录成功，则会返回user对象
	if user is not None:
		# 登录，在request中会保存user对象，在网页中可以使用
		auth.login(request, user)
		return redirect(referer)
	else:
		return render(request, 'error.html', {'message': '用户名或者密码不正确'})
	"""
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		# 数据有效
		if login_form.is_valid():
			# 获取user数据，该user数据在forms已经验证过，此时可以直接取出
			user = login_form.cleaned_data['user']
			# 登录
			auth.login(request, user)
			return redirect(request.GET.get('from', reverse('home')))
	else:
		login_form = LoginForm()
	context = dict()
	context['login_form'] = login_form
	return render(request, 'login.html', context=context)


def register(request):
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			username = register_form.cleaned_data['username']
			email = register_form.cleaned_data['email']
			password = register_form.cleaned_data['password_again']
			# 注册用户
			user = User.objects.create_user(username=username, password=password, email=email)
			user.save()

			user = auth.authenticate(username=username, password=password)
			auth.login(request, user)
	else:
		register_form = RegisterForm()

	context = dict()
	context['register_form'] = register_form
	return render(request, 'register.html', context=context)


def get_datas_from_cache(blog_content_type):
	# 今天热门博客排行，一个小时更新一次
	today_hot_data = cache.get('today_hot_data')
	if not today_hot_data:
		today_hot_data = get_today_hot_data(blog_content_type)
		cache.set('today_hot_data', today_hot_data, 60 * 60)

	# 昨天热门博客缓存
	yesterday_hot_data = cache.get('yesterday_hot_data')
	if not yesterday_hot_data:
		yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
		cache.set('yesterday_hot_data', yesterday_hot_data, 60 * 60 * 24)
	yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

	# 7天热门博客缓存数据
	seven_days_hot_data = cache.get('seven_days_hot_data')
	# 如果缓存数据为空
	if not seven_days_hot_data:
		# 得到数据
		seven_days_hot_data = get_7_days_hot_blogs()
		# 并写入缓存，以及设置缓存时间，以秒为单位
		# 缓存到期后，便会自动删除缓存，然后便会为None了
		cache.set('seven_days_hot_data', seven_days_hot_data, 60 * 60 * 24)
	# 30天热门博客缓存
	thirty_days_hot_data = cache.get('thirty_days_hot_data')
	if not thirty_days_hot_data:
		thirty_days_hot_data = get_30_days_hot_blogs()
		cache.set('thirty_days_hot_data', thirty_days_hot_data, 60 * 60 * 24)

	return today_hot_data, yesterday_hot_data, seven_days_hot_data, thirty_days_hot_data
