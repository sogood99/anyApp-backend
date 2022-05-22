from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class AccountTest(APITestCase):
    def setUp(self) -> None:
        self.test_user_data = {
            'username': 'testuser', 'email': 'test@test.com', 'password': 'testPassword'
        }
        self.test_user = User.objects.create_user(**self.test_user_data)
        self.test_token = Token.objects.create(user=self.test_user).key

        self.create_url = reverse('account-create')
        self.login_url = reverse('login')

    def test_create_user(self):
        data = {
            'username': 'foobar',
            'email': 'foo@email.com',
            'password': 'fooPass'
        }

        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        self.assertFalse('profile_name' in response.data)
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_login(self):
        response = self.client.post(
            self.login_url, self.test_user_data, format='json')
        self.assertEqual(response.data['token'], self.test_token)
