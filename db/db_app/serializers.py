from rest_framework import serializers
from db_app.models import Article, User, Contacts, Feedback

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('created', 'text', 'keywords', 'id', 'title', 'viewCount', 'likeCount',)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'userID', 'chatID', 'email', 'preferredLanguage', 'state', 'activationKey',)

class FeedbackSerializer(serializers.ModelSerializer):
	class Meta:
		model = Feedback
		fields = ('id', 'name', 'text', 'grade', 'email',)

class ContactsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contacts
		fields = ('info',)