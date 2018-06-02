from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import views
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status

from blog.models import Blog
from api.serializers import BlogSerializer, NewCommentListSerializer
from utils.hot_blog_util import *
from api.permissions import IsOwnerWriteOnly
from comment.models import NewCommentCount, Comment


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


class NewCommentCountAPIView(generics.RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return Response({'error': '请求错误'}, status=status.HTTP_400_BAD_REQUEST)
		new_comment_count = NewCommentCount.objects.filter(user=request.user).first()
		if new_comment_count:
			return Response({'new_comment_count': new_comment_count.count}, status=status.HTTP_200_OK)
		return Response({'new_comment_count': 0}, status=status.HTTP_200_OK)


class NewCommentListApiView(generics.RetrieveAPIView):
	serializer_class = NewCommentListSerializer
	permission_classes = [IsOwnerWriteOnly, ]

	def get_queryset(self):
		# 先根据登录用户，得到所有的博客
		blogs = Blog.objects.filter(author=self.request.user)
		comments = []
		# 遍历博客
		for blog in blogs:
			# 得到每篇博客的评论
			comment = Comment.objects.filter(object_id=blog.id)
			# 添加
			comments.extend(comment)
		return comments

	def get(self, request, *args, **kwargs):
		# 判断用户是否登录
		if request.user.is_authenticated:
			NewCommentCount.objects.get(user=request.user).clear_count()
		serializer = NewCommentListSerializer(self.get_queryset(), many=True)
		# 根据访问路径，返回json格式数据
		if request.path == '/api/newcommentlist/json/':
			return Response(serializer.data, status=status.HTTP_200_OK)
		# 返回数据到网页中
		context = dict()
		page = int(request.GET.get('page', -1))
		context['comments'] = serializer.data[page * 10:(page + 1) * 10]
		context['cur_page'] = int(self.request.GET.get('page', -1))
		return render(request, 'comment/comment_list.html', context=context)
