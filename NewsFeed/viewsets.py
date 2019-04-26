from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.permissions import IsAuthenticated
from . import serializers as srzs
from . import models as mdls
from . import permissions as perms
from .mixins import DisableListMixin, SetRequestUserOwnerOnCreateMixin


class SchoolViewSet(SetRequestUserOwnerOnCreateMixin, ModelViewSet):
    """
    학교 API
    
    retrieve:
    개별 학교 정보 조회
    
    list:
    전체 학교 목록 조회
    
    create:
    학교 생성
    
    update:
    학교 정보 수정
    
    partial_update:
    학교 정보 부분 수정
    
    delete:
    학교 삭제
    """
    serializer_class = srzs.SchoolSerializer
    permission_classes = (perms.IsOwnerOrReadOnly,)
    queryset = mdls.School.objects.all().order_by('name')   # 이름 오름차순
    
    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        """
        post:
        구독 설정
        """
        school = self.get_object()
        if school.subscribers.filter(pk=request.user.pk).exists():
            return Response('이미 구독 중 입니다.', status=HTTP_409_CONFLICT)
        school.subscribers.add(request.user)
        school.save()
        return Response('구독하였습니다.')

    @action(detail=True, methods=['delete'],
            permission_classes=(IsAuthenticated,))
    def unsubscribe(self, request, pk=None):
        """
        delete:
        구독 해제
        """
        school = self.get_object()
        if not school.subscribers.filter(pk=request.user.pk).exists():
            return Response('구독 중인 학교가 아닙니다.', status=HTTP_409_CONFLICT)
        school.subscribers.remove(request.user)
        school.save()
        return Response('구독을 취소 하였습니다.')


class ProfileViewSet(DisableListMixin, ModelViewSet):
    """
    로그인된 사용자의 프로필 API
    
    list:
    로그인된 사용자 프로필 조회
    
    create:
    사용자 프로필 추가
    
    update:
    로그인된 사용자 프로필 수정
    
    partial_update:
    로그인된 사용자 프로필 부분 수정
    
    delete:
    로그인된 사용자 탈퇴
    """
    permission_classes = (perms.IsSelf,)    # 본인만 사용 가능하도록 제한
    # 프로필 조회시 학교 목록을 함께 쿼리 해오도록 prefetch_related 추가
    queryset = mdls.User.objects \
        .prefetch_related('schools') \
        .filter(is_active=True)
    serializer_class = srzs.ProfileSerializer


class ArticleViewSet(DisableListMixin, SetRequestUserOwnerOnCreateMixin, ModelViewSet):
    """
    글 API
    
    retrieve:
    개별 글 조회
    
    list:
    전체 글 목록 조회
    
    create:
    글 생성
    
    update:
    글 수정
    
    partial_update:
    글 부분 수정
    
    delete:
    글 삭제
    """
    permission_classes = (perms.IsOwnerOrReadOnly,)
    serializer_class = srzs.ArticleSerializer
    queryset = mdls.Article.objects.all().order_by('-id')   # 최신글 내림차순
