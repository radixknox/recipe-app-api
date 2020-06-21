from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recipe.serializers import TagSerializer
from core.models import Tag,Ingredient
from django.conf import settings
from django.contrib.auth import get_user_model


TAG_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrive_tag_unauth(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@g.com',password='asdfgh',name='test')


        self.client.force_authenticate(self.user)


    def test_retrive_tag(self):
        """tags are retrived"""
        Tag.objects.create(user=self.user,name='vegan')
        Tag.objects.create(user=self.user,name='sweet')
        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_retrive_for_auth(self):
        """tags are retrived for authenticated user"""
        user1 = get_user_model().objects.create_user(email='test1@g.com',password='asdfgh1',name='test1')

        Tag.objects.create(user= user1,name='nonveg')
        tag = Tag.objects.create(user= self.user,name='vegan')
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'],tag.name)

    def test_create_tag(self):
        """test for creation of valid tag"""
        payload={'name':'vegan'}

        self.client.post(TAG_URL,payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    
