import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SchoolTangTest(APITestCase):
    """ Test module for SchoolTang API """
    
    def setUp(self):
        pass
    
    def test_register_users(self):
        """ 사용자 계정 생성 테스트 """
        pass
    
    def test_create_school_page(self):
        """ 학교 페이지 생성 테스트 """
        pass
    
    def test_subscribe_school(self):
        """ 학교 구독 테스트 """
        pass
    
    def test_get_subscribed_school_list(self):
        """ 구독된 학교 목록 조회 테스트 """
        pass
    
    def test_unsubscribe_school(self):
        """ 학교 구독 취소 테스트 """
        pass
    
    def test_write_article(self):
        """ 글 작성 테스트 """
        pass
    
    def test_read_newsfeed(self):
        """ 뉴스피드 조회 테스트 """
        pass
    
    def test_swagger_ui(self):
        """ Swagger UI 테스트 """
        pass
    
    def tearDown(self):
        pass
