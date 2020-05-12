from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from Auth.models import MyUser, ActivationChange, UserGroups


class Command(BaseCommand):
    help = 'Creates new expiration date for user for month'

    def handle(self, *args, **options):
        users = MyUser.objects.all()
        for user in users:
            user_groups = UserGroups.objects.filter(users=user)
            user_groups_names = ''
            if len(user_groups) != 0:
                for group in user_groups:
                    user_groups_names += group.name + " \n"
                activation = ActivationChange(user=user, activation_date=user.created, group_names=user_groups_names)
                activation.save()
