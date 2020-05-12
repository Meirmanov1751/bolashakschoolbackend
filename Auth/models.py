import uuid

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.urls import reverse
from .tasks import send_verification_email


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    class ROLES:
        STUDENT = 1
        TEACHER = 2
        ADMIN = 3

        ROLE_CHOICES = (
            (STUDENT, 'Студент'),
            (TEACHER, 'Учитель'),
            (ADMIN, 'Админ'),
        )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Фамилия')
    fathers_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=ROLES.ROLE_CHOICES, default=ROLES.STUDENT, verbose_name='Тип')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    is_verified = models.BooleanField(verbose_name='Подтверждение почты', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    device_id = models.CharField(max_length=300, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active_until = models.DateField('Активен до', null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self.__original_active_until = self.active_until

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return "%s %s %s" % (self.email, self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class ActivationChange(models.Model):
    user = models.ForeignKey('Auth.MyUser', on_delete=models.CASCADE)
    activation_date = models.DateField('Дата активации')
    group_names = models.TextField()


class UserGroups(models.Model):
    name = models.CharField('Имя группы', max_length=300)
    users = models.ManyToManyField('Auth.MyUser', verbose_name="Добавить пользователя", blank=True)
    sub_category = models.ManyToManyField('Lesson.SubCategory', verbose_name='Доступ к разделам', blank=True)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name


class Analytics(models.Model):
    created_date = models.DateField(auto_now_add=True, blank=True, null=True, verbose_name='дата создания')

    class Meta:
        verbose_name = 'Аналитика'
        verbose_name_plural = 'Аналитика'

    def __str__(self):
        return str(self.created_date)


class AnalyticsChild(models.Model):
    analytics = models.ForeignKey('Auth.Analytics', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='дата создания')
    user = models.ForeignKey('Auth.MyUser', verbose_name="Пользователь", on_delete=models.CASCADE, blank=True)
    path = models.URLField(verbose_name='Посещенная страница')

    class Meta:
        verbose_name = 'Детальная аналитика'
        verbose_name_plural = 'Детальная аналитика'

    def __str__(self):
        return "%s %s" % (self.created_date, self.user.email)


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_verification_email.delay(instance.pk)
# def user_pre_save(sender, instance, *args, **kwargs):
#     user = MyUser.objects.get(pk=instance.id)
#     if user.active_until != instance.active_until:
#         user_groups = UserGroups.objects.filter(users=instance)
#         user_groups_names = ''
#         for group in user_groups:
#             user_groups_names += group.name + " \n"
#         ActivationChange.objects.create(user=instance, activation_date=user.active_until, group_names=user_groups_names)

def analytics_child_post_save(sender, instance, signal, *args, **kwargs):
    date = instance.created_date.date()
    analytics = Analytics.objects.filter(created_date=date)
    post_save.disconnect(analytics_child_post_save, sender=sender)
    if len(analytics) == 0:
        analytics = Analytics.objects.create()
    else:
        analytics = analytics[0]
    instance.analytics = analytics
    instance.save()
    post_save.connect(analytics_child_post_save, sender=sender)

# signals.pre_save.connect(user_pre_save, sender=MyUser)
signals.post_save.connect(analytics_child_post_save, sender=AnalyticsChild)
signals.post_save.connect(user_post_save, sender=MyUser)
