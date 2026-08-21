from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для CustomUser без username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email обязателен"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # ВАЖНО: здесь мы НЕ передаём username
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # Убираем username из обязательных полей для входа, если нужно
    username = None

    # Email как поле для авторизации
    email = models.EmailField(unique=True, verbose_name="Email адрес")

    # Дополнительные поля
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Номер телефона"
    )
    country = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Страна"
    )

    # Указываем, что для авторизации используется email
    USERNAME_FIELD = "email"
    # Поля, которые будут запрашиваться при создании суперпользователя (кроме пароля)
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email
