from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, reset_password, verify_email, UserListView, toggle_activity

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('verify/<str:token>/', verify_email, name='verify'),
    path('reset_password/', reset_password, name='reset_password'),
    path('user/', UserListView.as_view(), name='list'),
    path('activity/<int:user_id>', toggle_activity, name='toggle_activity'),
    ]
