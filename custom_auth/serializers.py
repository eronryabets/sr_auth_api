from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            # по умолчанию активный пользователь (сделать подтверждение в почте)
            is_active=True
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        """
        Проверка, существует ли пользователь с такой же почтой.
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def update(self, instance, validated_data):
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
