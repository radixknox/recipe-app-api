from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

class AdminSiteTest(TestCase):


    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
        'admin@gmail.com',
        'test123')
        self.client.force_login(self.admin_user) #uses client function to
                                                 #login a user to the django system

        self.user = get_user_model().objects.create_user(
        email = 'testn@gmail.com',
        password = 'test123',
        name = 'testuser')

    def test_user_list(self):
        """Tests users are listed in Admin user """

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res,self.user.email)
        self.assertContains(res,self.user.name)

    def test_user_change(self):
        """Tests that edit user details page work """

        url = reverse('admin:core_user_change',args=[self.user.id])#if fieldsets not set then it will give call to the Default UserChange Page
        res = self.client.get(url)
        self.assertTrue(res.status_code, 200)

    def test_user_add(self):
        """tests that add user page works"""

        url = reverse('admin:core_user_add')#if add_fieldsets not set then it will give call to the Default UserChange Page
        res = self.client.get(url)
        self.assertTrue(res.status_code, 200)
