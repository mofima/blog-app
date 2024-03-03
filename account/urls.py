from django.urls import path 
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView

from . import views 
from .forms import LoginForm

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('login/', LoginView.as_view(template_name = 'account/login.html', authentication_form = LoginForm), name='login'),
    path('logout/', LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/', views.ResetConfirmPassword.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'), 
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'), 
]
