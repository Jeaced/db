from db_app.models import Article, User, Contacts
from db_app.serializers import ArticleSerializer, UserSerializer, ContactsSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

class ArticleList(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get(self, request, format=None):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ArticleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get_object(self, pk):
		try:
			return Article.objects.get(pk=pk)
		except Article.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		article = self.get_object(pk)
		serializer = ArticleSerializer(article)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		article = self.get_object(pk)
		serializer = ArticleSerializer(article, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):	
		article = self.get_object(pk)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleSearch(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get(self, request, keyword, format=None):
		articles = Article.objects.filter(keywords__contains=keyword)
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)

class ContactsDetail(APIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def get(self, request, format=None):
		contacts = Contacts.objects.all()
		serializer = ContactsSerializer(contacts, many=True)
		return Response(serializer.data)
	def post(self, request, format=None):
		if Contacts.objects.all().count() != 0:
			return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
		serializer = ArticleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def put(self, request, format=None):
		DEFAULT_PK = 1
		if Contacts.objects.all().count() != 1:
			return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
		info = Contacts.objects.get(pk=DEFAULT_PK)
		serializer = ContactsSerializer(info, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
