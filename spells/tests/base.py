from django.test import TestCase
from rest_framework.test import APIClient
from user.models import User


class APITestCase(TestCase):
    fixtures = ('spells.json', 'users.json')

    def setUp(self):
        self.user = User.objects.first()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
