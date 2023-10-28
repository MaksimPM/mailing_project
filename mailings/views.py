from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, TemplateView

from mailings.forms import MailingsForm, MessageForm, ClientForm
from mailings.models import Mailings, Message, Client, Log
from mailings.services import get_random_blog_article


class UserQuerysetMixin:
    """Ограничивает список просматриваемых пользователем объектов, принадлежащими только текущему пользователю,
     и сохраняет доступ для персонала"""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class StaffUserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам, и сохраняет доступ для персонала"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class UserObjectMixin:
    """Ограничивает доступ пользователя к чужим объектам"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


class UserFormMixin:
    """Присваивает объект пользователю"""

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LoginRequiredMessageMixin(LoginRequiredMixin):
    """Ограничение доступа для неавторизованных пользователей, вывод сообщения"""

    def handle_no_permission(self):
        messages.error(self.request, 'Для доступа к этой странице необходимо авторизоваться')
        return super().handle_no_permission()


def index(request):
    all_mailings = Mailings.objects.count()
    active_mailings = Mailings.objects.filter(is_active=True,
                                                status__in=[Mailings.STATUS_CHOICES[0],
                                                            Mailings.STATUS_CHOICES[1]]).count()
    clients = Client.objects.all().values('email').distinct().count()
    random_blog_article = get_random_blog_article()
    context = {
        'all_mailings': all_mailings,
        'active_mailings': active_mailings,
        'clients': clients,
        'blog_list': random_blog_article,
    }
    return render(request, 'mailings/index.html', context=context)


class ContactsView(TemplateView):
    template_name = 'mailings/clients_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            name = self.request.POST.get('name')
            email = self.request.POST.get('email')
            message = self.request.POST.get('message')
            print(f'You have new message from {name}({email}): {message}')
        context_data['object_list'] = Client.objects.all()
        return context_data


class MailingsCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Mailings
    form_class = MailingsForm
    permission_required = 'mailings.add_mailings'
    success_url = reverse_lazy('mailings:mailings_list')

    def get_form(self, form_class=None):
        """Формирование полей, принадлежащих текущему пользователю"""
        form = super().get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(user=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(user=self.request.user)

        return form


class MailingsUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Mailings
    form_class = MailingsForm
    permission_required = 'mailings.change_mailings'

    def get_success_url(self):
        return reverse('mailings:mailings_detail', args=[self.kwargs.get('pk')])


class MailingsListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Mailings
    permission_required = 'mailings.view_mailings'


class MailingsDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Mailings
    permission_required = 'mailings.view_mailings'


class MailingsDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Mailings
    permission_required = 'mailings.delete_mailings'
    success_url = reverse_lazy('mailings:mailings_list')


class MessageCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailings.add_message'
    success_url = reverse_lazy('mailings:message_list')


class MessageUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Message
    form_class = MessageForm
    permission_required = 'mailings.change_message'

    def get_success_url(self):
        return reverse('mailings:message_detail', args=[self.kwargs.get('pk')])


class MessageListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Message
    permission_required = 'mailings.view_message'


class MessageDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Message
    permission_required = 'mailings.delete_message'
    success_url = reverse_lazy('mailings:message_list')


class MessageDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Message
    permission_required = 'mailings.view_message'


class ClientCreateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserFormMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailings.add_client'
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailings.change_client'

    def get_success_url(self):
        return reverse('mailings:client_detail', args=[self.kwargs.get('pk')])


class ClientListView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserQuerysetMixin, ListView):
    model = Client
    permission_required = 'mailings.view_client'


class ClientDetailView(LoginRequiredMessageMixin, PermissionRequiredMixin, StaffUserObjectMixin, DetailView):
    model = Client
    permission_required = 'mailings.view_client'


class ClientDeleteView(LoginRequiredMessageMixin, PermissionRequiredMixin, UserObjectMixin, DeleteView):
    model = Client
    permission_required = 'mailings.delete_client'
    success_url = reverse_lazy('mailings:client_list')


@login_required
@permission_required('mailings.change_activity')
def toggle_activity(request, pk):
    """Отключение рассылок"""
    mailings = get_object_or_404(Mailings, pk=pk)
    if request.user.is_staff:
        if mailings.is_active:
            mailings.is_active = False
            mailings.status = mailings.STATUS_CHOICES[2]
            mailings.save()
        else:
            mailings.is_active = True
            mailings.status = mailings.STATUS_CHOICES[1]
            mailings.save()
        return redirect('mailings:mailings_list')


class LogListView(LoginRequiredMessageMixin, ListView):
    model = Log

    def get_queryset(self):
        """Получает список логов рассылок принадлежащих только текущему пользователю, и всех логов для персонала"""
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(mailing__user=self.request.user)


@login_required
def get_mailing_logs(request, pk):
    """Получение логов принадлежащих конкретной рассылке"""
    mailings_logs = Log.objects.filter(mailing_id=pk)
    mailings = mailings_logs.first().mailings
    context = {
        'object_list': mailings_logs,
        'mailings_name': mailings.name
    }
    return render(request, 'mailings/mailings_logs.html', context=context)
