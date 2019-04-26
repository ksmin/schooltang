from rest_framework.viewsets import ModelViewSet
from . import serializers as srzs
from . import models as mdls
from . import permissions as perms


class SchoolViewSet(ModelViewSet):
    serializer_class = srzs.SchoolSerializer
    permission_classes = (perms.IsSchoolOwner,)
    queryset = mdls.School.objects.all().order_by('name')
