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
            (TEACHER, 'Родитель'),
            (ADMIN, 'Админ'),
        )

    class LANGUAGES:
        KAZ = 1
        RUS = 2
        ENG = 3

        ROLE_CHOICES = (
            (KAZ, 'Казахский'),
            (RUS, 'Русский'),
            (ENG, 'Английский'),
        )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=255,
        unique=True,
    )
    parent_full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя Родителей')
    grade = models.IntegerField(verbose_name='Имя', default=6)
    full_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=ROLES.ROLE_CHOICES, default=ROLES.STUDENT, verbose_name='Тип')
    language = models.PositiveSmallIntegerField(choices=LANGUAGES.ROLE_CHOICES, default=LANGUAGES.RUS,
                                                verbose_name='Язык')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')
    is_verified = models.BooleanField(verbose_name='Подтверждение почты', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active_until = models.DateField('Активен до', null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    # баланс который может быть потрачен
    current_balance = models.FloatField(default=0)
    # баланс который будет храниться всегда, нужен для лидерборда
    full_balance = models.FloatField(default=0)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __init__(self, *args, **kwargs):
        super(MyUser, self).__init__(*args, **kwargs)
        self.__original_active_until = self.active_until

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return "%s %s " % (self.email, self.full_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def add_balance(self, balance):
        self.current_balance += balance
        self.full_balance += balance
        self.save()

    def minus_balance(self, balance):
        self.current_balance -= balance
        self.save()

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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


# signals.pre_save.connect(user_pre_save, sender=MyUser)
# signals.post_save.connect(analytics_child_post_save, sender=AnalyticsChild)
signals.post_save.connect(user_post_save, sender=MyUser)
