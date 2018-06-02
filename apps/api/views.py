from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status

from blog.models import Blog
from api.serializers import BlogSerializer
from utils.hot_blog_util import *
from api.permissions import IsOwnerWriteOnly


class HotBlogListView(generics.RetrieveAPIView):
	"""
	用来查询热门博客内容
	"""
	queryset = Blog.objects.all()
	serializer_class = BlogSerializer

	def get_queryset(self):
		hot_type = self.request.GET.get('type', -1)
		blog_content_type = ContentType.objects.get_for_model(Blog)
		context = get_datas_from_cache(blog_content_type, hot_type)
		# 从util接口中获取数据
		return context['hot_datas']

	def get(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		# 创建BlogSerializer对象，并传入数据
		serializer = BlogSerializer(queryset, many=True)
		print(serializer.data)
		return Response(serializer.data, status=status.HTTP_200_OK)


class BlogDetailAPIView(generics.RetrieveDestroyAPIView, generics.CreateAPIView):
	"""
	获取博客详细内容，或者创建，删除博客
	"""
	lookup_field = ['pk']
	serializer_class = BlogSerializer
	queryset = Blog.objects.all()

	permission_classes = [IsOwnerWriteOnly, ]

	def get_queryset(self):
		"""
		根据pk查询博客
		"""
		pk = int(self.request.GET.get('pk', -1))
		blog = Blog.objects.filter(pk=pk).first()
		print('blog = ', blog)
		return blog

	def get(self, request, *args, **kwargs):
		"""
		根据pk，返回具体博客内容
		"""
		queryset = self.get_queryset()
		if queryset is None:
			return Response({'error': '请求错误'}, status=status.HTTP_400_BAD_REQUEST)
		serializer = BlogSerializer(queryset)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		"""
		创建博客
		"""
		serializer = BlogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({'error': '创建失败'}, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		"""
		删除博客
		"""
		queryset: Blog = self.get_queryset()
		is_delete = queryset.delete()
		if is_delete:
			return Response({'success': '删除成功'}, status=status.HTTP_200_OK)
		return Response({'error': '删除失败'}, status=status.HTTP_400_BAD_REQUEST)
