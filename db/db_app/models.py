from django.db import models

class Article(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
	keywords = models.TextField()

	class Meta:
		ordering = ('created',)