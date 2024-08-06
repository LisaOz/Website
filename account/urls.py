from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login'),

    path('login/', auth_views.LoginView.as_view(), name='login'), # Login view from Django authentication framework
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Logout view ...
    path('', views.dashboard, name='dashboard'), # view for the dashboard
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'), # url for password change
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]
