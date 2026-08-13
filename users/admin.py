from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # 1. Исправляем ошибку: меняем сортировку с username на email
    ordering = ('email',)

    # 2. Меняем поле, отображаемое в списке и используемое для поиска
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

    # 3. Добавляем новые поля в форму редактирования
    # Берем стандартные поля UserAdmin и добавляем свои
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'phone_number', 'country')}),
    )

    # 4. Добавляем новые поля в форму создания пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {'fields': ('avatar', 'phone_number', 'country')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
