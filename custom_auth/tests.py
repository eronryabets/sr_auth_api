from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class AuthTests(APITestCase):

    def test_register_user(self):
        # Тестирование регистрации пользователя
        url = reverse('auth:register')
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # Создаем пользователя
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        # Тестирование входа пользователя
        url = reverse('auth:login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_access_protected_view(self):
        # Создаем пользователя и логинимся
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        url = reverse('auth:login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        access_token = response.data['access']

        # Пытаемся получить доступ к защищенному ресурсу
        protected_url = reverse('auth:user_profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
