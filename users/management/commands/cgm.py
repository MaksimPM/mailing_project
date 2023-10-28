from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create group Manager and User, add permissions'

    def handle(self, *args, **options):
        group_users, users_created = Group.objects.get_or_create(name='users')
        group_managers, managers_created = Group.objects.get_or_create(name='managers')
        if managers_created:
            permissions = Permission.objects.filter(content_type__model__in=['mailing', 'message', 'client', 'user']) \
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
                                                                                                        ])

            for perm in permissions:
                group_managers.permissions.add(perm)
            group_managers.user_set.update(is_staff=True)

            if users_created:
                permissions = Permission.objects.filter(
                    content_type__model__in=['mailing', 'message', 'client', 'user']) \
                                  .filter(name__icontains='view') | Permission.objects.filter(
                    codename__in=['change_mailings',
                                  'view_mailings',
                                  'add_mailings',
                                  'delete_mailings',
                                  'add_message',
                                  'change_message',
                                  'delete_message',
                                  'add_client',
                                  'change_client',
                                  'delete_client',
                                  ])

                for perm in permissions:
                    group_users.permissions.add(perm)
