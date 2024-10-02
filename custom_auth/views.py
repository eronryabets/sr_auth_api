from .models import CustomUser
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
import datetime
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status


# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # user_group = Group.objects.get(name='user')  # Назначаем группу по умолчанию
        # user.groups.add(user_group)


# Получение данных текущего пользователя
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': 'admin' if user.is_staff else 'user',
        })


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Аннулируем токен
        except Exception as e:
            pass  # В случае ошибки продолжаем

        response = Response({"message": "Logout successful"},
                            status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


# Логин и получение токенов
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # Получаем access и refresh токены
        access_token = data.get('access')
        refresh_token = data.get('refresh')

        # Создаем ответ с пустым телом (мы отправляем токены через cookies)
        response = JsonResponse({"message": "Login successful"})

        # Устанавливаем токены в httpOnly cookies
        access_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        refresh_expiry = datetime.datetime.utcnow() + datetime.timedelta(days=10)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,    # фронтенд будет пытаться получить токен через JS, что не рекомендуется
            secure=False,     # Установи True для HTTPS # Установите False для разработки
            samesite='Lax',   # Ограничивает отправку токенов в разных контекстах
            expires=access_expiry
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            expires=refresh_expiry
        )

        return response


# Обновление токена
class CookieTokenRefreshView(APIView):
    def post(self, request):
        # Извлекаем refresh_token из cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({"detail": "Refresh token missing in cookies"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Попытка создать новый access-токен из refresh-токена
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
        except InvalidToken:
            return Response({"detail": "Invalid refresh token"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Создаем ответ и отправляем новый access-токен в cookies
        response = Response({"access_token": str(access_token)},
                            status=status.HTTP_200_OK)

        access_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite='Lax',
            expires=access_expiry
        )

        return response
