from django.db import models
from django.contrib.auth.models import User
from . import mixins as mxs

REGION_NUMS = (
    ('02', '서울특별시'),
    ('031', '경기도'),
    ('032', '인천광역시'),
    ('033', '강원도'),
    ('041', '충청남도'),
    ('042', '대전광역시'),
    ('043', '충청북도'),
    ('044', '세종특별자치시'),
    ('051', '부산광역시'),
    ('052', '울산광역시'),
    ('053', '대구광역시'),
    ('054', '경상북도'),
    ('055', '경상남도'),
    ('061', '전라남도'),
    ('062', '광주광역시'),
    ('063', '전라북도'),
    ('064', '제주특별자치도')
)


class School(mxs.ManagementDateFieldsMixin, models.Model):
    owner = models.ForeignKey(User, verbose_name='관리자',
                              help_text='학교의 뉴스피드를 관리하는 책임자로써 학교를 '
                                        '생성한 사용자',
                              on_delete=models.PROTECT)
    name = models.CharField(max_length=256, verbose_name='학교명')
    region = models.CharField(max_length=8, verbose_name='시/군/구',
                              choices=REGION_NUMS)
    region_detail = models.CharField(max_length=128, verbose_name='지역 상세')
