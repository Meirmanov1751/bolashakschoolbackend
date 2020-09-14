import datetime

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
import logging
from OnlinePlatform.celery import app

@app.task
def send_forgot_email(user_id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        print(user.email)
        send_mail(
            'Восстановления аккаунта Bolashak Academy',
            'Рады приветствовать на нашем сайте. \n' +
            'Для того чтобы поменять пароль пройдите по ссылке: ' +
            'http://localhost:3000/%s' % (token),
            'yessenov.online@bk.ru',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        print('http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}))
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    # UserModel = get_user_model()
    # try:
    #     user = UserModel.objects.get(pk=user_id)
    #     print(user.email)
    #     send_mail(
    #         'Подтверждение аккаунта Yessenov Online',
    #         'Рады приветствовать на нашем сайте. \n' +
    #         'Для подтверждения регистрации пройдите по ссылке: ' +
    #         'https://api.yessenov-online.kz%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
    #         'yessenov.online@bk.ru',
    #         [user.email],
    #         fail_silently=False,
    #     )
    # except UserModel.DoesNotExist:
    #     logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)

@shared_task
def check_user_status_expired():
    UserModel = get_user_model()
    users = UserModel.objects.all()
    print('user status check')
    for user in users:
        if user.active_until is not None:
            if user.active_until < datetime.datetime.now().date() and user.is_active and not user.is_admin:
                user.is_active = False
                print(user.email + ' user is not active')
                user.save()
                try:
                    send_mail(
                        'Истичение срока действия аккаунта',
                        'В связи с тем что срок действия вашего аккаунта был исчерпан просим вас обратиться '+
                        ' к Администрации, либо же вашему учителю',
                        'yessenov.online@bk.ru',
                        [user.email],
                        fail_silently=False,
                        )
                except UserModel.DoesNotExist:
                    logging.warning("Tried to send verification email to non-existing user '%s'" % user.id)