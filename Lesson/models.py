from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Lesson.vimoe import upload


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    category = models.ForeignKey('Lesson.Category', on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return "%s %s" % (self.category.name, self.name)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Lesson(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    # video = models.FileField(null=True, blank=True)
    videoId = models.TextField(max_length=300, null=True, blank=True)
    vimeo = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    sub_category = models.ForeignKey('Lesson.SubCategory', on_delete=models.CASCADE, related_name='lessons', null=True)

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Homework(models.Model):
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, related_name='homeworks')
    file = models.FileField(blank=True, null=True)
    description = models.FileField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.lesson.name, self.id)

    class Meta:
        verbose_name = 'Решение Домашних задач'
        verbose_name_plural = 'Решение Домашних задач'


class LessonMaterial(models.Model):
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, related_name='lesson_materials')
    file = models.FileField()

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class UserLesson(models.Model):
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE, related_name='user_lessons')
    sub_category = models.ManyToManyField('Lesson.SubCategory', blank=True, verbose_name="Доступ к разделу")
    homework = models.ManyToManyField('Lesson.Homework', blank=True, verbose_name="Доступ к решению")

    def __str__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = 'Доступ к урокам'
        verbose_name_plural = 'Доступ к урокам'

#
# def uploadVideo(sender, instance, **kwargs):
#     post_save.disconnect(uploadVideo, sender=sender)
#     instance.videoId = upload(instance.video.path, instance.name)
#     instance.save()
#     post_save.connect(uploadVideo, sender=sender)
#
#
# post_save.connect(uploadVideo, sender=Lesson)
