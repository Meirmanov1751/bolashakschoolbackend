from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save

from Lesson.models import Lesson


class Analytics(models.Model):
    created_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'Аналитика'
        verbose_name_plural = 'Аналитика'

    def __str__(self):
        return str(self.created_date)


class AnalyticsCategory(models.Model):
    analytics = models.ForeignKey('Analytics.Analytics', on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey('Lesson.SubCategory', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Аналитика категории'
        verbose_name_plural = 'Аналитика категории'

    def __str__(self):
        return "%s %s" % (self.analytics.created_date, self.sub_category)
class AnalyticsLessonManager(models.Manager):
    def update_or_create(self, user, lesson):
        instance = self.get_queryset().filter(user=user).filter(lesson_id=lesson)
        # print('instance', instance)

        if len(instance) == 0:
            return super(AnalyticsLessonManager, self).create(user=user, lesson_id=lesson)
        # else:
        #     instance.

class AnalyticsLesson(models.Model):
    analytics_category = models.ForeignKey('Analytics.AnalyticsCategory', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='дата создания')
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='дата последнего посещения')
    user = models.ForeignKey('Auth.MyUser', verbose_name="Пользователь", on_delete=models.CASCADE, blank=True)
    lesson = models.ForeignKey('Lesson.Lesson', on_delete=models.CASCADE, null=True, blank=True, verbose_name='урок')
    class Meta:
        verbose_name = 'Аналитика уроков'
        verbose_name_plural = 'Аналитика уроков'

    def __str__(self):
        return "%s %s" % (self.created_date, self.user.email)

def analytics_child_post_save(sender, instance, signal, *args, **kwargs):
    date = instance.created_date.date()
    analytics = Analytics.objects.filter(created_date=date)
    analytics_category = AnalyticsCategory.objects.filter(sub_category=instance.lesson.sub_category)
    post_save.disconnect(analytics_child_post_save, sender=sender)
    if len(analytics) == 0:
        analytics = Analytics.objects.create()
    else:
        analytics = analytics[0]
    if len(analytics_category) == 0:
        lesson = Lesson.objects.get(pk=instance.lesson)
        analytics_category = AnalyticsCategory.objects.create(analytics=analytics, sub_category=lesson.sub_category)
    else:
        analytics_category = analytics_category[0]
    instance.analytics_category = analytics_category
    instance.save()
    post_save.connect(analytics_child_post_save, sender=sender)


signals.post_save.connect(analytics_child_post_save, sender=AnalyticsLesson)