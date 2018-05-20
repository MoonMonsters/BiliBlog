#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-16 21:45


from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	# 将评论功能的评论框设置为富文本模式
	# config_name，可以在settings中配置
	text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
	                       error_messages={'required': '评论内容不能为空'})

	def __init__(self, *args, **kwargs):
		# 将user数据通过创建CommentForm对象传入进来
		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		super(CommentForm, self).__init__(*args, **kwargs)

	def clean(self):
		# 判断用户是否登录
		if self.user.is_authenticated:
			self.cleaned_data['user'] = self.user
		else:
			raise forms.ValidationError('用户尚未登录')
		# 评论对象验证
		content_type = self.cleaned_data['content_type']
		object_id = self.cleaned_data['object_id']
		try:
			model_class = ContentType.objects.get(model=content_type).model_class()
			model_obj = model_class.objects.get(pk=object_id)
			self.cleaned_data['content_object'] = model_obj
		except ObjectDoesNotExist:
			raise forms.ValidationError('评论对象不存在')

		return self.cleaned_data
