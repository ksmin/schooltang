from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_409_CONFLICT, HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.permissions import IsAuthenticated
from . import serializers as srzs
from . import models as mdls
from . import permissions as perms


class SchoolViewSet(ModelViewSet):
    serializer_class = srzs.SchoolSerializer
    permission_classes = (perms.IsOwnerOrReadOnly,)
    queryset = mdls.School.objects.all().order_by('name')
    
    @action(detail=True, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        school = self.get_object()
        if school.subscribers.filter(pk=request.user.pk).exists():
            return Response('이미 구독 중 입니다.', status=HTTP_409_CONFLICT)
        school.subscribers.add(request.user)
        school.save()
        return Response('구독하였습니다.')

    @action(detail=True, methods=['delete'],
            permission_classes=(IsAuthenticated,))
    def unsubscribe(self, request, pk=None):
        school = self.get_object()
        if not school.subscribers.filter(pk=request.user.pk).exists():
            return Response('구독 중인 학교가 아닙니다.', status=HTTP_409_CONFLICT)
        school.subscribers.remove(request.user)
        school.save()
        return Response('구독을 취소 하였습니다.')


class ProfileViewSet(ModelViewSet):
    permission_classes = (perms.IsSelf,)    # 본인만 사용 가능하도록 제한
    # 프로필 조회시 학교 목록을 함께 쿼리 해오도록 prefetch_related 추가
    queryset = mdls.User.objects \
        .prefetch_related('schools') \
        .filter(is_active=True)
    serializer_class = srzs.ProfileSerializer
    
    def list(self, request, *args, **kwargs):
        """
        프로필 API를 통해 사용자 전체 목록이 조회 되는 것을 방지
        """
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
