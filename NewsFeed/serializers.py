from rest_framework.serializers import ModelSerializer
from . import models as mdls


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = mdls.School
        fields = ('id', 'owner', 'name', 'region', 'region_detail')
