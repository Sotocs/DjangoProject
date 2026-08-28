from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Delete and add test data"

    def handle(self, *args, **options):
        deleted_products, _ = Product.objects.all().delete()
        deleted_categories, _ = Category.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Удалено продуктов: {deleted_products}, категорий: {deleted_categories}"
            )
        )

        categories_data = [
            {"name": "Электроника", "description": "Гаджеты и техника"},
            {"name": "Книги", "description": "Художественная и техническая литература"},
            {"name": "Дом", "description": "Товары для дома и уюта"},
            {"name": "Смартфоны", "description": "Умные гаджеты"},
        ]

        categories = Category.objects.bulk_create(
            [Category(**data) for data in categories_data]
        )
        cat_map = {c.name: c for c in categories}

        self.stdout.write(self.style.SUCCESS("Категории созданы"))

        products_data = [
            {
                "name": "Наушники беспроводные",
                "description": "Комфортные наушники с шумоподавлением",
                "category": cat_map["Электроника"],
                "price": 12999.99,
            },
            {
                "name": "Умная колонка",
                "description": "Колонка с голосовым помощником и Wi‑Fi",
                "category": cat_map["Электроника"],
                "price": 8499.00,
            },
            {
                "name": "Книга «Изучаем Python»",
                "description": "Практическое руководство по Python",
                "category": cat_map["Книги"],
                "price": 899.00,
            },
            {
                "name": "Плед уютный",
                "description": "Мягкий плед, 150×200 см",
                "category": cat_map["Дом"],
                "price": 2499.50,
            },
            {
                "name": "Iphone 9 (учебный)",
                "description": "Нет в наличии, только для тестов",
                "category": cat_map["Смартфоны"],
                "price": 1000.00,
            },
        ]

        Product.objects.bulk_create([Product(**data) for data in products_data])

        self.stdout.write(self.style.SUCCESS("Тестовые продукты добавлены"))
