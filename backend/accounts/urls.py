
from django.urls import path
from  accounts.views import RegisterView,LogoutAPIView,LoginAPIView, PasswordTokenCheckAPI,RequestPasswordRestEmail,SetNewPasswordAPIView
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    # path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('logout1/', logoutView, name="logout1"),
    path('request-reset-email/', RequestPasswordRestEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('token_check/',tokencheck),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),name='password_reset_complete'),
    






]

