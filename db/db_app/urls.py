from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from db_app import views

urlpatterns = [
    url(r'^$', views.ArticleList.as_view()),
    url(r'^contact_info/', views.ContactsDetail.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
    url(r'^(?P<keyword>.+)/$', views.ArticleSearch.as_view()),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)