from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Course(models.Model):
    name = models.CharField('Имя', max_length=300)
    image = models.ImageField('Фото')
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Module(models.Model):
    course = models.ForeignKey('Course.Course', on_delete=models.CASCADE, verbose_name='Курс',
                               related_name='modules', null=True)
    name = models.CharField('Имя', max_length=300)
    image = models.ImageField(null=True)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

    def __str__(self):
        return "%s %s" % (self.course.__str__(), self.name)


class Category(models.Model):
    module = models.ForeignKey('Course.Module', on_delete=models.CASCADE, verbose_name='Категория',
                               related_name='categories', null=True)
    name = models.CharField('Имя', max_length=300)
    image = models.ImageField(null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return "%s %s" % (self.module.__str__(), self.name)


class Lesson(models.Model):
    category = models.ForeignKey('Course.Category', on_delete=models.CASCADE, related_name='lessons',
                                 null=True, verbose_name='Категория')
    name = models.CharField('Имя', max_length=300)
    description = models.TextField('Описание', blank=True, null=True)
    vimeo = models.TextField(null=True, blank=True)
    video = models.FileField(null=True)
    task_min = models.IntegerField('Минимум для прохода', null=True)
    free = models.BooleanField('Бесплатно', default=False)
    lesson_order = models.IntegerField('Позиция урока', default=0)

    lesson_balance_reward = models.FloatField(default=10)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonTasks(models.Model):
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

    lesson = models.ForeignKey('Course.Lesson', on_delete=models.CASCADE, related_name='tasks', verbose_name='Урок')
    name = models.CharField('Имя', max_length=300)
    description = RichTextField('Описание')
    correct = models.CharField('Правильный ответ', choices=TYPE.ROLE_CHOICES, default=TYPE.A, max_length=2)
    ans_a = RichTextField('Ответ А')
    ans_b = RichTextField('Ответ B')
    ans_c = RichTextField('Ответ С')
    ans_d = RichTextField('Ответ D')

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class LessonUserHistory(models.Model):
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Course.Lesson', on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)
    last_visited = models.DateTimeField(auto_now=True, null=True, blank=True)
    visited_count = models.IntegerField(default=0)
    is_rewarded = models.BooleanField(default=False)

class ModuleUser(models.Model):
    module = models.ForeignKey('Course.Module', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)

class ModulePrice(models.Model):
    module = models.ManyToManyField('Course.Module')
    price = models.IntegerField()
    name = models.CharField(max_length=300)
    description = models.TextField()

    class Meta:
        verbose_name = 'Цены за Модуль'
        verbose_name_plural = 'Цены за Модуль'
