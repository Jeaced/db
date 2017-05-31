from django.db import models

class Article(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=200, default='')
	viewCount = models.PositiveIntegerField(default=0)
	likeCount = models.PositiveIntegerField(default=0)
	text = models.TextField()
	keywords = models.TextField()
	relevance = models.FloatField(default=0)

	def save(self, **kwargs):
		self.relevance = self.likeCount/(self.viewCount + 1)
		super(Article, self).save()

class User(models.Model):
	LANGUAGE_CHOICES = (
		('EN', 'English'),
		('RU', 'Russian'),
		)
	alias = models.CharField(max_length=100)
	email = models.EmailField()
	preferredLanguage = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='EN')
	state = models.IntegerField(default=0)
	activationKey = models.CharField(max_length=100, default='')

class Feedback(models.Model):
	alias = models.CharField(max_length=100)
	text = models.TextField()

class Contacts(models.Model):
	info = models.TextField(default='')