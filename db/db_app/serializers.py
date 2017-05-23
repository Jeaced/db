from rest_framework import serializers
from db_app.models import Article

class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('created', 'text', 'keywords', 'id',)