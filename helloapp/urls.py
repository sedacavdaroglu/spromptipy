# howdy/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^search/$', views.search,name='search'),
    url(r'^back/$',views.back,name='back'),
       ]
