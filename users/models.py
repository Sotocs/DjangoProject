from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Убираем username из обязательных полей для входа, если нужно
    username = None

    # Email как поле для авторизации
    email = models.EmailField(unique=True, verbose_name='Email адрес')

    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')

    # Указываем, что для авторизации используется email
    USERNAME_FIELD = 'email'
    # Поля, которые будут запрашиваться при создании суперпользователя (кроме пароля)
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
