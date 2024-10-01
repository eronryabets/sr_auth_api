from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group


class AuthTests(APITestCase):

    def setUp(self):
        # Создаем группы user и admin для тестов
        Group.objects.create(name='user')
        Group.objects.create(name='admin')

    def test_register_user(self):
        # Тестирование регистрации пользователя
        url = reverse('custom_auth:register')
        data = {'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        # Создаем пользователя
        User.objects.create_user(username='testuser',
                                 email='testuser@example.com',
                                 password='testpassword123')

        # Тестирование входа пользователя с корректными данными
        url = reverse('custom_auth:login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка наличия access и refresh токенов в cookies
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_login_user_invalid_credentials(self):
        # Тестирование входа с неправильными данными
        url = reverse('custom_auth:login')
        data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.json()
        self.assertIn('detail', response_data)

    def test_access_protected_view(self):
        # Создаем пользователя и логинимся
        User.objects.create_user(username='testuser',
                                 email='testuser@example.com',
                                 password='testpassword123')
        url = reverse('custom_auth:login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')

        # Получаем токен из cookies
        access_token = response.cookies['access_token'].value

        # Пытаемся получить доступ к защищенному ресурсу
        protected_url = reverse('custom_auth:user_profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_protected_view_invalid_token(self):
        # Пытаемся получить доступ к защищенному ресурсу с неправильным токеном
        protected_url = reverse('custom_auth:user_profile')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
