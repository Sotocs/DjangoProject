from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает ей права'

    def handle(self, *args, **options):
        group_name = "Модератор продуктов"

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана.'))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Группа "{group_name}" уже существует, обновляем права.'
                )
            )

        # Получаем тип контента для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Список нужных разрешений (codename)
        permission_codenames = [
            "can_unpublish_product",  # твоё кастомное право из Meta.permissions
            "delete_product",  # стандартное право на удаление
        ]

        for codename in permission_codenames:
            try:
                perm = Permission.objects.get(
                    content_type=content_type, codename=codename
                )
                group.permissions.add(perm)
                self.stdout.write(f"  - Добавлено право: {perm.name}")
            except Permission.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(f'Не найдено разрешение с codename="{codename}"')
                )

        self.stdout.write(self.style.SUCCESS("Готово: группа и права настроены."))
