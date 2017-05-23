from django.db import models

class Article(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200, default='')
	viewCount = models.PositiveIntegerField(default=0)
	likeCount = models.PositiveIntegerField(default=0)
	text = models.TextField()
	keywords = models.TextField()

	class Meta:
		ordering = ('created',)

class User(models.Model):
	LANGUAGE_CHOICES = (
		('EN', 'English'),
		('RU', 'Russian'),
		)
	alias = models.CharField(max_length=100)
	email = models.EmailField()
	preferredLanguage = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')

class Contacts(models.Model):
	info = models.TextField(default='')