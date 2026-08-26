from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт суперпользователя по email (для CustomUser без username)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email", type=str, required=True, help="Email суперпользователя"
        )
        parser.add_argument("--password", type=str, required=True, help="Пароль")
        parser.add_argument("--first-name", type=str, default="", help="Имя")
        parser.add_argument("--last-name", type=str, default="", help="Фамилия")

    @transaction.atomic
    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]
        first_name = options.get("first_name", "")
        last_name = options.get("last_name", "")

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f"Пользователь с email {email} уже существует.")
            )
            return

        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        self.stdout.write(self.style.SUCCESS(f"Суперпользователь создан: {user.email}"))
