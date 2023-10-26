from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, verbose_name='Почта', unique=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=20, verbose_name='Страна', **NULLABLE)
    token = models.CharField(max_length=100, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = [
            (
                'set_activity',
                'Can change activity'
            )
        ]
