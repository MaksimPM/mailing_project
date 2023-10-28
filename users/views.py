import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.auth.models import Group


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        token = ''.join(random.sample(string.digits + string.ascii_letters, 12))
        self.object.token = token
        self.object.is_active = False
        self.object.save()
        url = 'http://127.0.0.1:8000/users/verify/' + token

        if form.is_valid():
            send_mail(
                subject='Подтверждение регистрации',
                message=f"""Для подтверждения регистрации и присоединении к команде перейдите по ссылке: {url}
                        Внимание! Если вы не понимаете, почему Вам пришло это письмо, просто проигнорируйте его""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        group = Group.objects.get(name='users')
        group.user_set.add(self.object)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'


def verify_email(request, token):
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()
        messages.success(request, 'Пользователь подтвержден')
    else:
        messages.error(request, 'Пользователь с таким e-mail не найден')
    return redirect('users:login')


def reset_password(request):
    if request.method == 'POST':
        input_email = request.POST.get('email')
        user = User.objects.filter(email=input_email).first()
        if user:

            password = User.objects.make_random_password()
            user.set_password(password)
            user.save(update_fields=['password'])
            send_mail(
                subject='Сброс пароля',
                message=f'''Вы успешно сбросили пароль для аккаунта {input_email}.\n Ваш новый пароль: {password}''',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[input_email]
            )
        else:
            messages.error(request, 'Пользователь с таким e-mail не найден')
    return render(request, 'users/reset_password.html')


@permission_required('users.set_activity')
@login_required
def toggle_activity(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.is_staff:
        if user.is_active and not user.is_superuser:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('users:list')
