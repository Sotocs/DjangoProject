from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    # Поля, которые будут видны при создании/редактировании пользователя
    # УБРАЛИ 'username', ДОБАВИЛИ 'email'
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name")}),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": (
                    "collapse",
                ),  # сворачивать блок прав, чтобы не занимал много места
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined"), "classes": ("collapse",)}),
    )

    # Список колонок в таблице пользователей в админке
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # По какому полю искать пользователей в админке (теперь только по email)
    search_fields = ("email", "first_name", "last_name")

    # Сортировка
    ordering = ("email",)

    # Важно: явно указываем, что username не используется
    readonly_fields = ()


# Регистрируем модель с нашим кастомным админ-классом
admin.site.register(User, CustomUserAdmin)
