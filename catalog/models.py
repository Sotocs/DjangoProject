from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Product(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PUBLISHED = "published"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Черновик"),
        (STATUS_PUBLISHED, "Опубликован"),
    ]

    name = models.CharField(max_length=100, verbose_name="наименование")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="products/", verbose_name="изображение", null=True, blank=True
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

    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="владелец",
        null=True,  # временно null=True, чтобы миграция прошла без запроса дефолта
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name="статус публикации",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["created_at", "updated_at"]
        permissions = [
            ("can_unpublish_product", "Может снимать продукт с публикации"),
        ]
