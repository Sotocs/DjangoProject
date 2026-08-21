from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Delete existing blog posts and add test data"

    def handle(self, *args, **options):
        # 1. Удаляем все существующие записи
        deleted_count, _ = Post.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Удалено записей блога: {deleted_count}"))

        # 2. Создаем тестового пользователя (если нет), чтобы у постов был автор
        # Если у тебя кастомная модель с email-автором, get_user_model() всё равно сработает корректно
        user, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("password123")
            user.save()
            self.stdout.write("Создан тестовый пользователь admin@example.com")

        # 3. Подготавливаем тестовые данные
        posts_data = [
            {
                "title": "Как начать изучать Django: первые шаги",
                "content": (
                    "Django — это мощный фреймворк на Python. В этой статье мы разберем, "
                    "как установить Django, создать первый проект и запустить сервер. "
                    "Вы узнаете про структуру проекта, приложения (apps) и базовые настройки. "
                    "Это идеальный старт для новичков, которые хотят создавать веб-приложения быстро и качественно."
                ),
                "created_at": timezone.now(),
                "is_published": True,
                "views": 150,
            },
            {
                "title": "Лучшие практики работы с PostgreSQL в Django",
                "content": (
                    "PostgreSQL — отличный выбор для Django-проектов. В статье рассмотрим, "
                    "как правильно настраивать подключение, использовать миграции, "
                    "оптимизировать запросы через select_related и prefetch_related, "
                    "а также работать с индексами и транзакциями для высокой производительности."
                ),
                "created_at": timezone.now(),
                "is_published": True,
                "views": 89,
            },
            {
                "title": "Почему стоит избегать глобальных переменных в Django?",
                "content": (
                    "Глобальные переменные могут казаться удобным решением, но в Django "
                    "они часто приводят к проблемам с многопоточностью и тестированием. "
                    "Разберем реальные кейсы, где глобальные переменные ломают логику приложения, "
                    "и покажем, какие альтернативы (контекстные процессоры, сигналы, сервисы) "
                    "лучше использовать вместо них."
                ),
                "created_at": timezone.now(),
                "is_published": False,  # Черновик
                "views": 0,
            },
            {
                "title": "Обзор новых возможностей Django 6.0",
                "content": (
                    "В последней версии Django появилось много интересного: улучшения в админке, "
                    "новые инструменты для асинхронности, обновленные шаблоны форм и многое другое. "
                    "Мы собрали главные изменения, которые стоит учесть при обновлении проектов, "
                    "и разобрали примеры кода для быстрого внедрения."
                ),
                "created_created_at": timezone.now(),  # Опечатка исправлена ниже
                "is_published": True,
                "views": 230,
            },
            {
                "title": "Секреты быстрой разработки на Django: лайфхаки от профи",
                "content": (
                    "Хотите разрабатывать быстрее? В этой статье делимся проверенными приемами: "
                    "использование CBV, правильная структура папок, автоматизация тестов, "
                    "интеграция с CI/CD и советы по отладке. Эти методы помогут вам экономить часы работы "
                    "и делать код чище и понятнее."
                ),
                "created_at": timezone.now(),
                "is_published": True,
                "views": 312,
            },
        ]

        # Исправляем опечатку в словаре выше (ключ created_created_at -> created_at)
        # В реальном коде лучше сразу писать правильно, здесь исправляю для надежности:
        for post in posts_data:
            if "created_created_at" in post:
                post["created_at"] = post.pop("created_created_at")

        # 4. Массово создаем записи
        # Примечание: поле author нужно добавить вручную, так как в bulk_create нельзя передать связанные объекты напрямую
        # Поэтому сначала создаем объекты без автора, а потом обновляем

        # Вариант А (простой, если поле author не обязательно): создаем как есть
        # Но у тебя в модели Post нет поля author, значит, всё ок!

        posts = [Post(**data) for data in posts_data]
        Post.objects.bulk_create(posts)

        self.stdout.write(self.style.SUCCESS("Тестовые записи блога добавлены"))
