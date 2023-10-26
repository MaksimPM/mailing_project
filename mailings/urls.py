from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import *

app_name = MailingsConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('mailings/list/', cache_page(60)(MailingsListView.as_view()), name='mailings_list'),
    path('mailings/<int:pk>/', MailingsDetailView.as_view(), name='mailings_detail'),
    path('mailings/create/', MailingsCreateView.as_view(), name='mailings_create'),
    path('mailings/<int:pk>/update/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('mailings/<int:pk>/delete/', MailingsDeleteView.as_view(), name='mailings_delete'),
    path('client/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('contacts/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailings/<int:pk>/toggle_activity', toggle_activity, name='mailing_toggle_activity'),
    path('logs/', LogListView.as_view(), name='logs'),
    path('logs/<int:pk>/', get_mailing_logs, name='mailing_logs'),
    path('contacts/', ContactsView.as_view(), name='contacts')
]
