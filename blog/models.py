from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержимое')
    preview_image = models.ImageField('Превью', upload_to='blog/previews/', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=False)
    views = models.PositiveIntegerField('Просмотры', default=0)

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

