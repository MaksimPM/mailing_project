from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create group Manager, add permissions'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='manager')
        if created:
            permissions = Permission.objects.filter(content_type__model__in=['mailing', 'message', 'client', 'user'])\
                .filter(name__icontains='view') | Permission.objects.filter(codename__in=['set_activity',
                                                                                          'change_activity',
                                                                                          'change_mailings',
                                                                                          'view_mailings',
                                                                                          'add_mailings',
                                                                                          'delete_mailings',
                                                                                          'add_message',
                                                                                          'change_message',
                                                                                          'delete_message',
                                                                                          'add_client',
                                                                                          'change_client',
                                                                                          'delete_client',
                                                                                          'view_admin'])

            for perm in permissions:
                group.permissions.add(perm)
