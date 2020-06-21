from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

class ModelTests(TestCase):

    def sample_user(self):
        return get_user_model().objects.create_user(email='test@g.com',
                                                  name='test',
                                                  password='test1234')


    def test_create_user_with_email(self):
        """tests user created with email"""

        email = 'aniketpatil1799@gmail.com'
        password = 'test123'
        name = 'godo'

        user = get_user_model().objects.create_user(
        email = email,
        password = password,
        name= name
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_no_email_provided(self):
        """Tests for email not provided"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test123','name')


    def test_create_new_superuser(self):
        """tests if user is superuser"""

        email = 'test@gmail.com'
        password= 'test123'

        user = get_user_model().objects.create_superuser(email,password)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

def test_ingredint_str(self):
    ingredient = models.Ingredient.objects.create(user=sample_user(),name='cucumber')
    self.assertEqual(str(ingredient),'cucumber')
