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

    def get_count_subscribers(self):
        return Subscription.objects.filter(author=self).count()

    def get_count_subscriptions(self):
        return Subscription.objects.filter(subscriber=self).count()

    def get_is_subscribed(self, author):
        is_subscribed = False
        if self != author:
            is_subscribed = Subscription.objects.filter(
                subscriber=self,
                author=author
            ).exists()
        return is_subscribed


class Subscription(models.Model):
    subscriber = models.ForeignKey('Coder', on_delete=models.CASCADE, related_name='subscriptions', verbose_name='Подписчик')
    author = models.ForeignKey('Coder', on_delete=models.CASCADE, related_name='subscribers', verbose_name='Автор')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('subscriber', 'author')  # предотвращаем дубликаты

    def __str__(self):
        return f"{self.subscriber} → {self.author}"