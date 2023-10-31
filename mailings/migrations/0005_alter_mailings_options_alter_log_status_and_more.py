# Generated by Django 4.2.6 on 2023-10-30 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailings', '0004_rename_mailings_log_mailing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailings',
            options={'ordering': ('-id',), 'permissions': [('change_activity', 'Change activity')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterField(
            model_name='log',
            name='status',
            field=models.CharField(choices=[('completed', 'Завершена'), ('created', 'Создана'), ('running', 'Запущена')], max_length=10, verbose_name='Статус попытки'),
        ),
        migrations.AlterField(
            model_name='mailings',
            name='frequency',
            field=models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=50, verbose_name='Периодичность'),
        ),
        migrations.AlterField(
            model_name='mailings',
            name='status',
            field=models.CharField(choices=[('completed', 'Завершена'), ('created', 'Создана'), ('running', 'Запущена')], default='created', max_length=50, verbose_name='Статус рассылки'),
        ),
    ]