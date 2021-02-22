from django.urls import path,include
from django.conf.urls import include, url
from rest_framework import routers
from . import views
from .views import MemeViewSet,MemeFilterViewSet
from rest_framework import renderers
from rest_framework.routers import DefaultRouter



#trailing slash is set to false for assessment url endpoints
router = DefaultRouter(trailing_slash=False)

#set of urls using views of MemeViewSet mapped to assessment url endpoints
router.register(r'memes', MemeViewSet, basename='memes')

#set of urls using views of MemeFilterViewSet mapped to custom url endpoints in deployed app
router.register(r'memefilters', MemeFilterViewSet, basename='memefilters')
urlpatterns = router.urls
