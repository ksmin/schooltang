from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import viewsets as st_viewsets


router = SimpleRouter()
router.register(r'schools', st_viewsets.SchoolViewSet)
router.register(r'profile', st_viewsets.ProfileViewSet, basename='profile')
router.register(r'articles', st_viewsets.ArticleViewSet)
router.register(r'newsfeed', st_viewsets.NewsFeedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
