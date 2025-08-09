from django.contrib.auth.models import AbstractUser
# from posts.models import Tags
from django.db import models


class Coder(AbstractUser):
    photo = models.ImageField(upload_to='users_photo', verbose_name='Аватарка', blank=True, null=True,
                              default='users_photo/no_ava.jpg')
    birthday = models.DateTimeField(blank=True, null=True, verbose_name='Дата Рождения')
    about = models.TextField(verbose_name='Мини-Биография')
    email = models.EmailField(unique=True, max_length=254, verbose_name='E-mail', db_index=True)

    # Связь с моделями
    # favorite_tags = models.ManyToManyField(Tags, related_name='users')

    class Meta:
        db_table = 'Coder'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'