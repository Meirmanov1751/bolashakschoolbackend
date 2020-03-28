from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField()


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey('Lesson.Category', on_delete=models.CASCADE, related_name='sub_category')


class Lesson(models.Model):
    name = models.CharField(max_length=500)
    video = models.FileField(null=True, blank=True)
    vimeo_url = models.URLField(null=True, blank=True)
    image = models.ImageField()


class LessonMaterial(models.Model):
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, related_name='lesson_materials')
    file = models.FileField()


@receiver(post_save, sender=Lesson, dispatch_uid="upload_to_vimeo")
def update_stock(sender, instance, **kwargs):

