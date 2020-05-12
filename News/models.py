from django.db import models
from mdeditor.fields import MDTextField
# Create your models here.
class News(models.Model):
    title = models.TextField('Название')
    image = models.ImageField('Изображение')
    description = MDTextField()

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новости"