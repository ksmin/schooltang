from django.db import models
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class ManagementDateFieldsMixin(models.Model):
    class Meta:
        abstract = True
        
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='생성일시',
                                        help_text='항목이 생성된 시점으로 자동 추가')
    date_modified = models.DateTimeField(auto_now=True, verbose_name='수정일시',
                                         help_text='항목이 수정된 시점으로 수정시 자동 변경')


class DisableListMixin(object):
    """
    ViewSet의 list 메소드를 재정의 하여 목록이 조회되는 것을 방지
    """

    def list(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


class SetRequestUserOwnerOnCreateMixin(object):
    """
    
    """
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
