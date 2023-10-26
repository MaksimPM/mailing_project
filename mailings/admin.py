from django.contrib import admin

from mailings.models import Mailings, Client, Log, Message


# Register your models here.
@admin.register(Mailings)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'time', 'frequency', 'status')
    list_filter = ('time', 'start_date', 'frequency', 'status',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'email')
    list_filter = ('fullname', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime', 'status', 'server_response', 'mailing')
    list_filter = ('mailing', 'status', 'datetime')
