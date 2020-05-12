from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from Auth.models import MyUser

class Command(BaseCommand):
    help = 'Creates new expiration date for user for month'

    def handle(self, *args, **options):
        users = MyUser.objects.all()
        for user in users:
            user.active_until = user.created.date() + timedelta(days=30)
            user.save()
