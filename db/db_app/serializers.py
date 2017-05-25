from rest_framework import serializers
from db_app.models import Article, User, Contacts

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('created', 'text', 'keywords', 'id', 'title', 'viewCount', 'likeCount',)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'alias', 'email', 'preferredLanguage',)

class ContactsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contacts
		fields = ('info',)