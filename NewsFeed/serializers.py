from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models as st_models


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = st_models.School
        fields = ('id', 'owner', 'name', 'region', 'region_detail')
        read_only_fields = ('owner',)   # owner는 SchoolViewSet에서 자동 입력


class SchoolCompactSerializer(ModelSerializer):
    class Meta:
        model = st_models.School
        fields = ('id', 'name', 'region')


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = st_models.User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password', 'date_joined', 'last_login', 'schools')
        read_only_fields = ('id', 'date_joined', 'last_login', 'schools')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    schools = SchoolCompactSerializer(many=True, read_only=True)  # 구독 중인 학교 목록
    
    def validate_password(self, value):
        """ 패스워드와 확인용 패드워드가 동일한지 확인 """
        if (
            'password_confirm' not in self.initial_data or
            value != self.initial_data['password_confirm']
        ):
            raise serializers.ValidationError('A entered password does not '
                                              'match with password_confirm.')
        return value


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = st_models.Article
        fields = ('id', 'school', 'owner', 'content',
                  'date_created', 'date_modified')
        read_only_fields = ('owner',)   # owner는 ArticleViewSet에서 자동 입력
        
    def validate_school(self, value):
        """
        글을 작성하려는 학교 페이지의 소유자만 글을 작성 가능.
        :param value: 학교 오브젝트
        :return: Validation 검증된 학교 오브젝트
        """
        if value.owner != self.context['request'].user:
            raise serializers.ValidationError("글 작성 권한이 없습니다.")
        return value
