from django.contrib.auth import get_user_model
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='email')
    fullname = models.CharField(max_length=150, verbose_name='Клиент')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='Клиент', **NULLABLE)

    def __str__(self):
        return f'{self.fullname} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailings(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название рассылки', **NULLABLE)
    start_date = models.DateField(default=False, verbose_name='Дата рассылки')
    time = models.TimeField(default='00:00', verbose_name='Время рассылки')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default=FREQUENCY_CHOICES[0],
                                 verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0],
                              verbose_name='Статус рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Получатели')
    is_active = models.BooleanField(default=True, verbose_name='Активность рассылки')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name}({self.pk}): {self.get_frequency_display()}, {self.get_status_display()}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'change_activity',
                'Change activity'
            )
        ]


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма', **NULLABLE)
    content = models.TextField(verbose_name='Содержание', **NULLABLE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Log(models.Model):
    STATUS_LOG = [
        ('success', 'Успешно'),
        ('failure', 'Ошибка'),
    ]

    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=10, choices=Mailings.STATUS_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, verbose_name='Рассылка')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, default=0, verbose_name='Письмо')

    def __str__(self):
        return f'Рассылка {self.mailing}, статус: {self.status}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
