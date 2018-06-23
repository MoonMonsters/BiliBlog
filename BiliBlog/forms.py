#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-15 22:52


from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',
	                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
	# 设置为密码格式
	password = forms.CharField(label='密码',
	                           widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

	captcha = CaptchaField(label='验证码')

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		# 对用户名和密码验证
		user = auth.authenticate(username=username, password=password)
		if user is None:
			# 验证失败，抛出错误
			raise forms.ValidationError('用户名或密码不正确')
		else:
			# 验证成功，写入cleaned_data中
			self.cleaned_data['user'] = user
		# 需要返回cleaned_data数据
		return self.cleaned_data


class RegisterForm(forms.Form):
	username = forms.CharField(label='用户名',
	                           max_length=30,
	                           min_length=3,
	                           widget=forms.TextInput(
		                           attrs={'class': 'form-control', 'placeholder': '请输入用户名'}
	                           ))
	password = forms.CharField(label='密码',
	                           min_length=6,
	                           widget=forms.PasswordInput(
		                           attrs={'class': 'form-control', 'placeholder': '请输入密码'}
	                           ))
	password_again = forms.CharField(label='密码',
	                                 min_length=6,
	                                 widget=forms.PasswordInput(
		                                 attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}
	                                 ))
	email = forms.EmailField(label='邮箱',
	                         widget=forms.EmailInput(
		                         attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}
	                         ))
	captcha = CaptchaField(label='验证码')

	def clean_username(self):
		"""
		对用户进行验证
		"""
		username = self.cleaned_data['username']
		# 判断用户名是否存在
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名已存在')
		return username

	def clean_email(self):
		email = self.cleaned_data['username']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('用户名已存在')
		return email

	def clean_password_again(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError('两次输入的密码不一致')
		return password_again
