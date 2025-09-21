from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify


def create_slug_ru_to_eng(slug):
    letters = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y',
        'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', '.': '-'}
    return slugify(''.join([letters.get(l.lower(), l) for l in slug]))


class Post(models.Model):

    class Status(models.TextChoices):
        CHECK = ('check', 'На проверке')
        APPROVED = ('approved', 'одобрено')
        BLOCKED = ('blocked', 'заблокировано')

    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=350, verbose_name='Краткое описание')
    content = models.TextField(max_length=5000, verbose_name='Содержание поста')
    image = models.ImageField(upload_to='posts_image', verbose_name='Изображение')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    data_update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    status = models.TextField(choices=Status.choices, default=Status.CHECK)
    moderator_comment = models.CharField(max_length=255, blank=True, default='')

    # Связь с моделями
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='posts')
    tags = models.ManyToManyField('Tags', related_name='posts')
    coder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='post')

    class Meta:
        db_table = 'Post'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('post_by_slug', args=[self.slug])

    def __str__(self):
        return self.title

    def get_maybe_like_post(self):
        # same_category_posts = Post.objects.filter(category=self.category).exclude(pk=self.pk)
        same_tags_posts = Post.objects.filter(tags__in=self.tags.all()).exclude(pk=self.pk).distinct()
        # maybe_like_posts = (same_category_posts | same_tags_posts).distinct()
        return same_tags_posts.prefetch_related('tags')[:4]

    def get_likes_count(self):
        return self.user_reactions.filter(reaction_type=Reaction.ReactionType.LIKE).count()

    def get_dislikes_count(self):
        return self.user_reactions.filter(reaction_type=Reaction.ReactionType.DISLIKE).count()

    def save(self, **kwargs):
        self.slug = create_slug_ru_to_eng(self.title)
        return super().save(**kwargs)


class Category(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    title = models.CharField(max_length=255, verbose_name='Название', unique=True)

    class Meta:
        db_table = 'Category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('post_by_category', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = create_slug_ru_to_eng(self.title)
        return super().save(**kwargs)


class Tags(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    title = models.CharField(max_length=255, verbose_name='Название', unique=True)

    class Meta:
        db_table = 'Tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def get_absolute_url(self):
        return reverse('post_by_tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = create_slug_ru_to_eng(self.title)
        return super().save(**kwargs)


class Reaction(models.Model):
    class ReactionType(models.IntegerChoices):
        LIKE = 1, 'лайк'
        DISLIKE = 0, 'дизлайк'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='post_reactions'
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='user_reactions'
    )
    reaction_type = models.IntegerField(choices=ReactionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Реакция на пост'
        verbose_name_plural = 'Реакции на посты'