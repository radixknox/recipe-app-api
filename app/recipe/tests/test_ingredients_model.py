from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.conf import settings
from core.models import Ingredient
from django.contrib.auth import get_user_model
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

class TestIngriedientModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@g.com',
                                                        name='test',
                                                        password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        Ingredient.objects.create(user=self.user,name='adrak')
        Ingredient.objects.create(user=self.user,name='cinnamon')

        res = self.client.get(INGREDIENT_URL)
        ingre = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingre,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_retrive_for_auth(self):
        """test retrive ingredient list for auth user"""
        user1 = get_user_model().objects.create_user(email='test1@g.com',
                                                        name='test1',
                                                        password='test123')
        ingre = Ingredient.objects.create(user=self.user,name='adrak')
        Ingredient.objects.create(user=user1,name='cinnamon')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.data[0]['name'],ingre.name)

    def test_create_ingredient(self):
        """test for creating ingredient"""
        payload = {'name':'cinamon'}
        self.client.post(INGREDIENT_URL,payload)
        exists = Ingredient.objects.filter(name=payload['name'],
                                           user=self.user
                                           ).exists()
        self.assertTrue(exists)
