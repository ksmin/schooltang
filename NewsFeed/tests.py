import random
import timeit
# from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from . import models as st_models


class UserRegistrationTest(APITestCase):
    """ Test module for user registration """
    
    def setUp(self) -> None:
        self.url = '/profile/registration/'
        
        self.pw_confirm_not_exist_data = {
            'username': 'pw_confirm_not_exist_user',
            'first_name': 'pw_confirm',
            'last_name': 'not exist',
            'email': 'pw_cne@gmail.com',
            'password': 'pw_cneDkagh',
        }
        
        self.wrong_pw_data = {
            'username': 'wrong_pw_user',
            'first_name': 'wrong',
            'last_name': 'password',
            'email': 'wp@gmail.com',
            'password': 'wpDkagh',
            'password_confirm': 'wpPw',
        }

        self.dummy_user_data = {
            'username': 'tester',
            'first_name': 'tester',
            'last_name': 'tester',
            'email': 'tester@schooltang.com',
            'password': 'testerDkagh',
            'password_confirm': 'testerDkagh',
        }
        
        self.mass_user_data = [{
            'username': f'tester_{i}',
            'first_name': str(i),
            'last_name': 'tester',
            'email': f'tester_{i}@schooltang.com',
            'password': f'testerDkagh{i}',
            'password_confirm': f'testerDkagh{i}',
        } for i in range(20)]

    def test_password_confirmation_not_exist(self):
        """ 사용자 가입 중 확인용 비밀번호 부재 검증 테스트 """
        response = self.client.post(self.url, self.pw_confirm_not_exist_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)
    
    def test_wrong_password_confirmation(self):
        """ 사용자 가입 중 확인용 비밀번호 오류 검증 테스트 """
        response = self.client.post(self.url, self.wrong_pw_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)
    
    def test_register_users(self):
        """ 사용자 계정 생성 테스트 """
        response = self.client.post(self.url, self.dummy_user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_expected = {**self.dummy_user_data}
        response_expected.pop('password')
        response_expected.pop('password_confirm')
        self.assertEqual(response.data, response_expected)
        # start_time = timeit.default_timer()
        # for user_data in self.dummy_user_data:
        #     print('user_data:', user_data.get('username'))
        #     response = self.client.post(self.url, user_data, format='json')
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print('count:', st_models.User.objects.count())
        # time_takes = timeit.default_timer() - start_time
        # print('time_takes:', time_takes, 'sec.')
        # self.assertEqual(st_models.User.objects.count(),
        #                  len(self.dummy_user_data))


class SchoolPageTest(APITestCase):
    """ Test module for SchoolTang API """
    
    def setUp(self):
        self.urls = {
            'school': '/schools/',
            'profile': '/profile/',
            'article': '/articles/',
            'newsfeed': '/newsfeed/',
        }
        self.factory = APIRequestFactory()
        self.school_page_owner = st_models.User.objects.create_user(
            'school_page_owner', email='school_page_owner@schooltang.com',
            password='school_page_ownerDkagh')
        self.subscriber1 = st_models.User.objects.create_user(
            'subscriber1', email='subscriber1@schooltang.com',
            password='subscriber1Dkagh')
        self.subscriber2 = st_models.User.objects.create_user(
            'subscriber2', email='subscriber2@schooltang.com',
            password='subscriber2Dkagh')
        self.school1 = st_models.School.objects.create(
            name='school1', region=random.choice(st_models.REGION_NUMS)[0],
            region_detail='detila info', owner=self.school_page_owner)
        
        self.school_data = {
            'name': 'test school',
            'region': random.choice(st_models.REGION_NUMS)[0],
            'region_detail': 'test region detail',
        }
        self.article_data = {
            'school': self.school1.id,
            'content': '테스트 글입니다.',
        }
    
    def test_create_school_page(self):
        """ 학교 페이지 생성 테스트 """
        self.client.login(username='school_page_owner',
                          password='school_page_ownerDkagh')
        school_count = st_models.School.objects.count()
        response = self.client.post(self.urls.get('school'), self.school_data,
                                    format='json')
        response_expected = {**response.data}
        school_id = response_expected.pop('id')
        _ = response_expected.pop('owner')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_expected, self.school_data)
        school_created = st_models.School.objects.get(pk=school_id)
        self.assertEqual(self.school_page_owner, school_created.owner)
        self.assertEqual(school_count + 1, st_models.School.objects.count())
    
    def test_subscribe_school(self):
        """ 학교 구독 & 목록 조회 & 구독 취소 테스트 """
        self.client.login(username='subscriber1', password='subscriber1Dkagh')
        response = self.client.get(self.urls.get('profile'))
        subscribed_school_count = len(response.data.get('schools'))
        
        # 학교 구독
        subscribe_url = \
            f"{self.urls.get('school')}{self.school1.id}/subscribe/"
        response = self.client.post(subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, '구독하였습니다.')
        response = self.client.post(subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, '이미 구독 중 입니다.')
        self.assertEqual(
            1, st_models.Subscribe.objects.filter(user=self.subscriber1,
                                                  school=self.school1).count()
        )

        # 구독된 학교 목록 조회
        response = self.client.get(self.urls.get('profile'))
        schools_subscribed = response.data.get('schools')
        self.assertEqual(subscribed_school_count + 1, len(schools_subscribed))
        self.assertEqual(
            schools_subscribed[0].get('id'),
            self.school1.id
        )
        
        # 구독 취소
        unsubscribe_url = \
            f"{self.urls.get('school')}{self.school1.id}/unsubscribe/"
        response = self.client.delete(unsubscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, '구독을 취소 하였습니다.')
        response = self.client.get(self.urls.get('profile'))
        schools_subscribed = response.data.get('schools')
        self.assertEqual(subscribed_school_count, len(schools_subscribed))
        response = self.client.delete(unsubscribe_url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data, '구독 중인 학교가 아닙니다.')
    
    def test_write_article_and_newsfeed(self):
        """ 글 작성 & 뉴스피드 조회 테스트 """
        # 구독
        self.client.login(username='subscriber2', password='subscriber2Dkagh')
        response = self.client.get(self.urls.get('newsfeed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        newsfeed_article_count = response.data.get('count')
        subscribe_url = \
            f"{self.urls.get('school')}{self.school1.id}/subscribe/"
        self.client.post(subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        
        # 글 작성
        self.client.login(username='school_page_owner',
                          password='school_page_ownerDkagh')
        response = self.client.post(self.urls.get('article'),
                                    self.article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_response = response.data
        created_article_id = expected_response.pop('id')
        expected_response.pop('date_created')
        expected_response.pop('date_modified')
        owner_id = expected_response.pop('owner')
        self.assertEqual(self.article_data, response.data)
        self.assertEqual(self.school_page_owner.id, owner_id)
        self.client.logout()
        
        # 뉴스피드 조회
        self.client.login(username='subscriber2', password='subscriber2Dkagh')
        response = self.client.get(self.urls.get('newsfeed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsfeed_article_count + 1,
                         response.data.get('count'))
        expected_response = response.data.get('results')[0]
        article_id = expected_response.pop('id')
        self.assertEqual(created_article_id, article_id)
        expected_response.pop('date_created')
        expected_response.pop('date_modified')
        expected_response.pop('owner')
        self.assertEqual(self.article_data, expected_response)
