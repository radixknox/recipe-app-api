from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """tests for all kind of Users"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """tests that a valid user is created"""
        payload = {
                    'email':'test@gmail.com',
                    'password':'test123',
                    'name':'Test name'

        }
        res = self.client.post(CREATE_USER_URL,payload)
        user = get_user_model().objects.get(**res.data) #the user is returned and now we test if a valid user is created ornot
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_already_exists(self):
        """test that duplicate users not present"""
        payload = {
                    'email':'test1@gmail.com',
                    'password':'test1293',
                    'name':'Testname'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_user_password_length(self):
        """tests that the user has password length > 5"""
        payload = {
                    'email':'test@gmail.com',
                    'password':'tes',
                    'name':'Test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
        email = payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """tests if the token is created once user is created"""
        payload = {
                    'email':'test@gmail.com',
                    'password':'test123'
        }

        payload1 = {
                    'email':'test@gmail.com',
                    'password':'test123',
                    'name':'test'
        }

        create_user(**payload1)
        res = self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.data)
        self.assertTrue(res.status_code,status.HTTP_200_OK)

    def test_token_invalid_credentials(self):
        """test for invalid credentials provide failure"""
        create_user(email='aniket@gmail.com',password='test123',name='ani')
        payload ={
                'email':'aniket@gmail.com',
                'password':'wrong'
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token',res.data)

    def test_token_created_no_user(self):
        """token if user does not exist token is not created"""
        payload ={
                'email':'aniket@gmail.com',
                'password':'wrong'
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_email_pass_provided(self):
        """test that email and password is provided"""
        create_user(email='aniket@gmail.com',name='test',password='test123')
        payload = {
                    'email':'test@gmail.com',
                    'password': ''
        }
        res = self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_retrieve_unauth_user(self):
        """test authentication required for access"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTestUserApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            name ='test',
            email='test@gmail.com',
            password ='testpass'
        )
        self.client.force_authenticate(user=self.user)
    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_ME_not_allowed(self):
        """tests theat post request not allowed"""
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_updated(self):

        payload={
            'name' : 'test1',
            'password': 'newpassword'
        }
        res = self.client.patch(ME_URL,payload)
        self.user.refresh_from_db()   #update the db with new test_create_valid_user_success
        #self.assertEqual(res.data,{
            #'name': payload['name'],
        #})
        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
