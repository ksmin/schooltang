from rest_framework.viewsets import ModelViewSet
from . import serializers as srzs
from . import models as mdls


class SchoolViewSet(ModelViewSet):
    serializer_class = srzs.SchoolSerializer
    queryset = mdls.School.objects.all()
