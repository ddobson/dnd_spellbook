from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User


class APITestCase(TestCase):
    fixtures = ('spells.json', 'users.json')

    def setUp(self):
        self.user = User.objects.create(
            email="primary@email.com",
            password="primarysecret",
            is_active=True,
            is_admin=False,
        )
        self.secondary_user = User.objects.create(
            email="secondary@email.com",
            password="secondarysecret",
            is_active=True,
            is_admin=False,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
