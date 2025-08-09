from django.contrib.sitemaps import Sitemap
from .models import Post, Category, Tags


class PostsMap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9

    def items(self):
        return Post.objects.all()


class CategoryMap(Sitemap):
    changefreq = 'yearly'
    priority = 0.6

    def items(self):
        return Category.objects.all()


class TagsMap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Tags.objects.all()