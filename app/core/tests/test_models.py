from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """tests user created with email"""

        email = 'aniketpatil1799@gmail.com'
        password = 'test123'

        user = get_user_model().objects.create_user(
        email = email,
        password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_no_email_provided(self):
        """Tests for email not provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123')


    def test_create_new_superuser(self):
        """tests if user is superuser"""

        email = 'test@gmail.com'
        password= 'test123'

        user = get_user_model().objects.create_superuser(email,password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
