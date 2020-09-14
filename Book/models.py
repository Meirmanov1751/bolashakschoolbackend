from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField('Имя', max_length=300)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    sale_price = models.IntegerField('Цена со скидкой')
    sale = models.BooleanField('Скидка',default=False)
    cover = models.ImageField('Обложка')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class BookImages(models.Model):
    book = models.ForeignKey('Book.Book', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()
