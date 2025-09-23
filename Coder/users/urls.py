from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView,
                                       PasswordChangeView, PasswordChangeDoneView
                                       )
from django.urls import path, reverse_lazy
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:pk_user>', views.ProfileUser.as_view(), name='profile'),
    path('profile/edit/', views.EditAccountUser.as_view(), name='profile_edit'),
    path('my_subscribers/', views.MySubscribers.as_view(), name='my_subscribers'),
    path('my_subscriptions/', views.MySubscriptions.as_view(), name='my_subscriptions'),
    path('toggle_subscription/', views.toggle_subscription, name='toggle_subscription'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='users/forms.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done', PasswordResetDoneView.as_view(
        template_name='users/email_send_success.html'
    ), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='users/forms.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset/complete', PasswordResetCompleteView.as_view(
        template_name='users/success_change_password.html'
    ), name='password_reset_complete'),

    path('password-change/', PasswordChangeView.as_view(
        template_name='users/forms.html',
        extra_context={'title': 'Смена Пароля', 'btn_title': 'Изменить'},
        success_url=reverse_lazy('users:password_change_done')
    ), name='password_change'),

    path('password-change/done', PasswordChangeDoneView.as_view(
        template_name='users/success_change_password.html'
    ), name='password_change_done')
]