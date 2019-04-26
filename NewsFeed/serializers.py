from rest_framework.serializers import ModelSerializer
from . import models as mdls


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = mdls.School
        fields = ('id', 'owner', 'name', 'region', 'region_detail')


class SchoolCompactSerializer(ModelSerializer):
    class Meta:
        model = mdls.School
        fields = ('id', 'name', 'region')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = mdls.User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'date_joined', 'last_login', 'schools')
        
    schools = SchoolCompactSerializer(many=True)    # 구독 중인 학교 목록을 조회
