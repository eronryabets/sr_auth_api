import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Менеджер для модели `CustomUser`, предоставляющий методы создания пользователей и суперпользователей.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет нового пользователя с указанными данными.

        :param username: Имя пользователя.
        :type username: str
        :param email: Электронная почта пользователя.
        :type email: str
        :param password: Пароль пользователя (опционально).
        :type password: str or None
        :param extra_fields: Дополнительные поля для модели `CustomUser`.
        :type extra_fields: dict
        :return: Созданный экземпляр пользователя.
        :rtype: CustomUser
        :raises ValueError: Если не указана электронная почта.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет нового суперпользователя с указанными данными.

        :param username: Имя суперпользователя.
        :type username: str
        :param email: Электронная почта суперпользователя.
        :type email: str
        :param password: Пароль суперпользователя (опционально).
        :type password: str or None
        :param extra_fields: Дополнительные поля для модели `CustomUser`.
        :type extra_fields: dict
        :return: Созданный экземпляр суперпользователя.
        :rtype: CustomUser
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, расширяющая возможности стандартной модели Django.

    Атрибуты:
        - `id` (UUIDField): Уникальный идентификатор пользователя.
        - `username` (CharField): Имя пользователя, уникальное.
        - `email` (EmailField): Электронная почта пользователя, уникальная.
        - `is_active` (BooleanField): Активен ли пользователь.
        - `is_staff` (BooleanField): Является ли пользователь сотрудником (имеет доступ к админ-панели).
        - `is_superuser` (BooleanField): Является ли пользователь суперпользователем.
        - `objects` (CustomUserManager): Менеджер для модели `CustomUser`.
        - `USERNAME_FIELD` (str): Поле, используемое для аутентификации (в данном случае `username`).
        - `REQUIRED_FIELDS` (list): Список полей, необходимых при создании суперпользователя.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        """
        Возвращает строковое представление пользователя, используя его имя.

        :return: Имя пользователя.
        :rtype: str
        """
        return self.username
