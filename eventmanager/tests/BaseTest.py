from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user and get its token
        self.user1 = get_user_model().objects.create_user(
            username="test1", password="test1"
        )
        self.token1 = Token.objects.create(user=self.user1)

        # Create another user
        self.user2 = get_user_model().objects.create_user(
            username="test2", password="test2"
        )
        self.token2 = Token.objects.create(user=self.user2)
