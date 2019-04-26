from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import viewsets as vsets


router = DefaultRouter()
router.register(r'schools', vsets.SchoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
