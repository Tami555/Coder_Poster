import json

from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView

from .forms import LoginUserForm, RegistrationUserForm, EditAccountUserForm
from .models import Subscription
from .utils import DataFormMixin


class LoginUser(DataFormMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title_page = 'Вход & Авторизация'
    btn_title = 'Войти'

    def get_success_url(self):
        return reverse('all_posts')


class RegistrationUser(DataFormMixin, CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/forms.html'
    title_page = 'Регистрация'
    btn_title = 'Зарегаться'

    def get_success_url(self):
        return reverse('users:login')


@login_required(login_url='users:login')
def logout_user(request: HttpRequest):
    logout(request)
    return redirect('all_posts')


class ProfileUser(DataFormMixin, DetailView):
    template_name = 'users/profile.html'
    pk_url_kwarg = 'pk_user'
    context_object_name = 'coder'
    title_page = ''

    def get_object(self, queryset=None):
        coder = get_user_model().objects.get(pk=self.kwargs['pk_user'])
        self.title_page = f'Аккаунт {coder.username}'
        return coder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_context_mixin(context, title=self.title_page)


class EditAccountUser(DataFormMixin, LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    form_class = EditAccountUserForm
    model = get_user_model()
    login_url = 'users:login'
    title_page = 'Редактирование профиля'
    btn_title = 'Сохранить изменения'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile', args=[self.request.user.pk])


class MySubscribers(LoginRequiredMixin, ListView):
    template_name = 'users/list_user.html'
    context_object_name = 'coders'

    def get_queryset(self):
        return get_user_model().objects.filter(
            subscriptions__author=self.request.user
        ).select_related().prefetch_related('subscriptions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши подписчики'
        context['phrase'] = "Подписчики — это команда, которая поддерживает твой творческий полет"
        return context


class MySubscriptions(LoginRequiredMixin, ListView):
    template_name = 'users/list_user.html'
    context_object_name = 'coders'

    def get_queryset(self):
        return get_user_model().objects.filter(
            subscribers__subscriber=self.request.user
        ).select_related().prefetch_related('subscribers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваши подписки'
        context['phrase'] = "Ваши подписки — это любимые уголки, где всегда ждут с новыми идеями."
        return context


# обработки подписки
@require_POST
@login_required
def toggle_subscription(request):
    try:
        data = json.loads(request.body)
        author_id = data.get('author_id')
        action = data.get('action')

        author = get_object_or_404(get_user_model(), id=author_id)

        if request.user == author:
            return JsonResponse({
                'success': False,
                'message': 'Нельзя подписаться на себя'
            })

        if action == 'subscribe':
            subscription, created = Subscription.objects.get_or_create(
                subscriber=request.user,
                author=author
            )
            if created:
                return JsonResponse({
                    'success': True,
                    'message': 'Подписка оформлена'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Вы уже подписаны'
                })

        elif action == 'unsubscribe':
            deleted, _ = Subscription.objects.filter(
                subscriber=request.user,
                author=author
            ).delete()

            if deleted:
                return JsonResponse({
                    'success': True,
                    'message': 'Подписка отменена'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Подписка не найдена'
                })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Ошибка сервера'
        })