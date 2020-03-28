from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    category = models.ForeignKey('Lesson.Category', on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return "%s %s" % (self.category.name, self.name)


class Lesson(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(null=True, blank=True)
    vimeo_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    sub_category = models.ForeignKey('Lesson.SubCategory', on_delete=models.CASCADE, related_name='lessons', null=True)

    def __str__(self):
        return "%s" % (self.name)


class Homework(models.Model):
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, related_name='homeworks')
    file = models.FileField(blank=True, null=True)
    description = models.FileField(blank=True, null=True)

    def __str__(self):
        return "%s %s" % (self.lesson.name, self.id)


class LessonMaterial(models.Model):
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, related_name='lesson_materials')
    file = models.FileField()


class UserLesson(models.Model):
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE, related_name='user_lessons')
    sub_category = models.ManyToManyField('Lesson.SubCategory', blank=True)
    homework = models.ManyToManyField('Lesson.Homework', blank=True)

    def __str__(self):
        return "%s" % self.user
