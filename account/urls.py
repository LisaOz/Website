from django.contrib.auth import views as auth_views
from django.urls import path #, include - for the  Django provide URL patterns
from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')), - Django provided URL pattern


    #path('login/', views.user_login, name='login'),

    path('login/', auth_views.LoginView.as_view(), name='login'), # Login view from Django authentication framework
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Logout view ...
    
    path('', views.dashboard, name='dashboard'), # view for the dashboard
    
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'), # url for password change
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), # urls fr reset password
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # tocken
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register/', views.register, name='register'), 

    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'), 
    path('users/follow/', views.user_follow, name='user_follow'), 
    path('users/<username>/', views.user_detail, name='user_detail'), # This URL detail pattern will be used to generate the canonical URL for users

]
