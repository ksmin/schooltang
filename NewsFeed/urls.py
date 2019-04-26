from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import viewsets as vsets


router = SimpleRouter()
router.register(r'schools', vsets.SchoolViewSet)
router.register(r'profile', vsets.ProfileViewSet)
router.register(r'articles', vsets.ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
