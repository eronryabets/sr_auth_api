from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Этот сериализатор обрабатывает создание нового пользователя, включая валидацию данных
    и установку пароля с хешированием. Предназначен для использования в представлениях регистрации.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Создаёт нового пользователя с хешированным паролем.

        :param validated_data: Валидированные данные для создания пользователя.
        :type validated_data: dict
        :return: Созданный экземпляр пользователя.
        :rtype: CustomUser
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # по умолчанию активный пользователь (сделать подтверждение в почте)
            is_active=True
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения основных данных пользователя.

    Используется для представления информации о пользователе без включения чувствительных данных,
    таких как пароль.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя.

    Позволяет обновлять электронную почту и пароль пользователя. Обеспечивает валидацию
    уникальности электронной почты и безопасное обновление пароля.
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        """
        Проверяет, что новая электронная почта уникальна среди всех пользователей,
        за исключением текущего пользователя.

        :param value: Новая электронная почта.
        :type value: str
        :return: Проверенная электронная почта.
        :rtype: str
        :raises serializers.ValidationError: Если электронная почта уже используется другим пользователем.
        """
        user_id = self.instance.id
        if CustomUser.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
        """
        Обновляет профиль пользователя, включая электронную почту и пароль.

        :param instance: Экземпляр пользователя, который будет обновлён.
        :type instance: CustomUser
        :param validated_data: Валидированные данные для обновления пользователя.
        :type validated_data: dict
        :return: Обновлённый экземпляр пользователя.
        :rtype: CustomUser
        """
        # Обновление почты
        email = validated_data.get('email', None)
        if email:
            instance.email = email

        # Обновление пароля, если передано новое значение
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
