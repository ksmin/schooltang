from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_409_CONFLICT
from rest_framework.permissions import IsAuthenticated
from . import serializers as srzs
from . import models as mdls
from . import permissions as perms


class SchoolViewSet(ModelViewSet):
    serializer_class = srzs.SchoolSerializer
    permission_classes = (perms.IsSchoolOwner,)
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
