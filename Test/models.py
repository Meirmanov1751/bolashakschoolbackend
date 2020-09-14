from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.
class TestCategory(models.Model):
    name = models.CharField('Имя', max_length=300)
    image = models.ImageField('Фото')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class TestGroup(models.Model):
    category = models.ForeignKey('Test.TestCategory', on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='test_groups')
    name = models.CharField(max_length=300)
    free = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return "%s %s" % (self.category.__str__(), self.name)


class TestGroupCategory(models.Model):
    test_group = models.ForeignKey('Test.TestGroup', on_delete=models.CASCADE, verbose_name='Тест',
                                   related_name='test_group_categories')
    name = models.CharField('Имя', max_length=300)
    image = models.ImageField(null=True)
    duration = models.IntegerField()
    pass_min = models.IntegerField()

    class Meta:
        verbose_name = 'Категории тестов'
        verbose_name_plural = 'Категории тестов'

    def __str__(self):
        return "%s %s" % (self.test_group.__str__(), self.name)


class TestTasks(models.Model):
    class TYPE:
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        ROLE_CHOICES = (
            (A, 'A'),
            (B, 'B'),
            (C, 'C'),
            (D, 'D'),
        )

    group_category = models.ForeignKey('Test.TestGroupCategory', on_delete=models.CASCADE, related_name='tests',
                                       verbose_name='Категория')
    name = models.CharField('Имя', max_length=300)
    description = RichTextField('Описание')
    correct = models.CharField('Правильный ответ', choices=TYPE.ROLE_CHOICES, default=TYPE.A, max_length=2)
    ans_a = RichTextField('Ответ А')
    ans_b = RichTextField('Ответ B')
    ans_c = RichTextField('Ответ С')
    ans_d = RichTextField('Ответ D')

    class Meta:
        verbose_name = 'Вопросы тестов'
        verbose_name_plural = 'Вопросы тестов'


class TestGroupUser(models.Model):
    group = models.ForeignKey('Test.TestGroup', on_delete=models.CASCADE)
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    verified = models.BooleanField(default=False)