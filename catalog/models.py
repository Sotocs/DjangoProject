from django.db import models

# Create your models here.
# Выполните следующие запросы:
# Получите все категории.
# Получите все продукты.
# Найдите все продукты в определенной категории.
# Обновите цену для определенного продукта.
# Удалите продукт.

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="catalog/images", verbose_name="изображение", null=True, blank=True
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="категория"
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name="цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="дата последнего изменения"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["created_at", "updated_at"]



