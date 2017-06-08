from django.core.urlresolvers import reverse
from db_app import views
from db_app.models import Article, User, Contacts, Feedback
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User as US

class ArticleTests(APITestCase):
	def setUp(self):
		US.objects.create(username='admin')

	def test_create_article(self):
		"""
		Ensure we can create new Article object
		"""
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		url = '/db/'
		data = {'title': 'TestArticle', 'viewCount': '3', 'likeCount': '1'}
		response = client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Article.objects.count(), 1)
		self.assertEqual(Article.objects.get().title, 'TestArticle')
		self.assertEqual(Article.objects.get().relevance, 0.25)

	def test_change_article(self):
		"""
		Ensure we can change Article objects
		"""
		article = Article.objects.create()
		user = US.objects.get(username='admin')
		data = {'title': 'ChangedTitle'}
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.put('/db/1/', data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Article.objects.get().title, 'ChangedTitle')

	def test_delete_article(self):
		"""
		Ensure we can delete Article objects
		"""
		article = Article.objects.create()
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.delete('/db/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Article.objects.count(), 0)

	def test_get_article(self):
		"""
		Ensure we can get Article objects
		"""
		article = Article.objects.create(title='TestArticle')
		client = APIClient()
		response = client.get('/db/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], 'TestArticle')

	def test_search_article(self):
		"""
		Ensure we can search Article using keywords
		"""
		article = Article.objects.create(keywords='test', viewCount=5, likeCount=0)
		article = Article.objects.create(keywords='keyword', viewCount=7, likeCount=1, title='2nd most relevant')
		article = Article.objects.create(keywords='article', viewCount=4, likeCount=2, title='most relevant')
		article = Article.objects.create(keywords='not found', viewCount=5, likeCount=5)
		client = APIClient()
		response1 = client.get('/db/test&keyword&article/', format='json')
		response2 = client.get('/db/wrongkeyword/', format='json')
		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response1.data), 2)
		self.assertEqual(response1.data[0]['title'], 'most relevant')
		self.assertEqual(response1.data[1]['title'], '2nd most relevant')
		self.assertEqual(response2.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response2.data), 0)

	def test_like_increment(self):
		"""
		Ensure we can increment likes using likeIncrement view
		"""
		article = Article.objects.create(viewCount=4, likeCount=1)
		client = APIClient()
		response = client.post('/db/like_increment/1/', format='json')
		self.assertEqual(Article.objects.get().likeCount, 2)
		self.assertEqual(Article.objects.get().relevance, 0.4)

	def test_view_increment(self):
		"""
		Ensure we can increment views using viewIncrement view
		"""
		article = Article.objects.create(viewCount=3, likeCount=2)
		client = APIClient()
		response = client.post('/db/view_increment/1/', format='json')
		self.assertEqual(Article.objects.get().viewCount, 4)
		self.assertEqual(Article.objects.get().relevance, 0.4)

class UserTests(APITestCase):
	def setUp(self):
		US.objects.create(username='admin')

	def test_create_user(self):
		"""
		Ensure we can create new User object
		"""
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		data = {'email': 'test_user'}
		response1 = client.post('/db/users/', data, format='json')
		response2 = client.post('/db/users/', data, format='json')
		self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(User.objects.count(), 1)
		self.assertEqual(User.objects.get().email, 'test_user')

	def test_change_user(self):
		"""
		Ensure we can change User objects
		"""
		user_object1 = User.objects.create(email='test_user1')
		user_object2 = User.objects.create(email='test_user2')
		user = US.objects.get(username='admin')
		data = {'email': 'changed_email'}
		client = APIClient()
		client.force_authenticate(user=user)
		response1 = client.put('/db/users/1/', data, format='json')
		response2 = client.put('/db/users/2/', data, format='json')
		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(User.objects.get(pk=1).email, 'changed_email')

	def test_delete_user(self):
		"""
		Ensure we can delete User objects
		"""
		user_object = User.objects.create(email='test_user')
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.delete('/db/users/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(User.objects.count(), 0)

	def test_get_user(self):
		"""
		Ensure we can get User objects
		"""
		user_object = User.objects.create(email='test_user')
		client = APIClient()
		response = client.get('/db/users/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['email'], 'test_user')

	def test_search_user(self):
		"""
		Ensure we can search User objects using email field
		"""
		user_object1 = User.objects.create(email='test_user1')
		user_object2 = User.objects.create(email='test_user2')
		client = APIClient()
		response1 = client.get('/db/users/test_user1/', format='json')
		response2 = client.get('/db/users/wrong_email/', format='json')
		self.assertEqual(response1.status_code, status.HTTP_200_OK)
		self.assertEqual(response1.data['email'], 'test_user1')
		self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

class ContactsTests(APITestCase):
	def setUp(self):
		US.objects.create(username='admin')

	def test_change_contacts(self):
		"""
		Ensure we can add and change contact info
		"""
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		data = {'info': 'test_info'}
		response = client.put('/db/contact_info/', data, format='json')
		self.assertEqual(Contacts.objects.get().info, 'test_info')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		data = {'info': 'changed_info'}
		response = client.put('/db/contact_info/', data, format='json')
		self.assertEqual(Contacts.objects.get().info, 'changed_info')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_contacts(self):
		"""
		Ensure we can get contact info
		"""
		contacts = Contacts.objects.create(info='test_info')
		client = APIClient()
		response = client.get('/db/contact_info/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]['info'], 'test_info')

class FeedbackTests(APITestCase):

	def setUp(self):
		US.objects.create(username='admin')

	def test_create_feedback(self):
		"""
		Ensure we can create new Feedback object
		"""
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		data = {'email': 'test_user'}
		response = client.post('/db/feedback/', data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Feedback.objects.count(), 1)
		self.assertEqual(Feedback.objects.get().email, 'test_user')

	def test_change_feedback(self):
		"""
		Ensure we can change Feedback objects
		"""
		feedback = Feedback.objects.create(email='test_user')
		user = US.objects.get(username='admin')
		data = {'email': 'changed_email'}
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.put('/db/feedback/1/', data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Feedback.objects.get().email, 'changed_email')

	def test_delete_feedback(self):
		"""
		Ensure we can delete Feedback objects
		"""
		feedback = Feedback.objects.create(email='test_user')
		user = US.objects.get(username='admin')
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.delete('/db/feedback/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertEqual(Feedback.objects.count(), 0)

	def test_get_feedback(self):
		"""
		Ensure we can get Feedback objects
		"""
		feedback = Feedback.objects.create(email='test_user')
		client = APIClient()
		response = client.get('/db/feedback/1/', format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['email'], 'test_user')