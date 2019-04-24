from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import viewsets as vsets


router = SimpleRouter()
router.register(r'schools', vsets.SchoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
]
