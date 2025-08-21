from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError


def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Ассоциирует аккаунт социальной сети с существующим пользователем по электронной почте
    или отображает сообщение об ошибке, если email уже зарегистрирован.
    """
    if user:
        return None

    email = details.get('email')
    if email:
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            # Ассоциируем аккаунт социальной сети с существующим пользователем
            return {'user': user, 'is_new': False}
        except ObjectDoesNotExist:
            try:
                user = User.objects.create_user(username=email, email=email)
                return {'user': user, 'is_new': True}
            except IntegrityError:
                messages.error(kwargs['request'], "Аккаунт с такой почтой уже зарегистрирован. Войдите, используя форму регистрации, или используйте другую почту для входа через Google.")
                return redirect(reverse('users:login'))
    return None


def social_group(backend, user, response, *args, **kwargs):
    gr = Group.objects.filter(name='social')
    if len(gr):
        user.groups.add(gr[0])