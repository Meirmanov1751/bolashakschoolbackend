from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
import logging

from OnlinePlatform.celery import app


@app.task
def send_verification_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        print(user.email)
        send_mail(
            'Подтверждение аккаунта Yessenov Online',
            'Рады приветствовать на нашем сайте. \n' +
            'Для подтверждения регистрации пройдите по ссылке: ' +
            'https://api.yessenov-online.kz%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'yessenov.online@bk.ru',
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
