from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Tags


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['show_photo', 'title', 'description', 'image', 'data_update']
    list_display_links = ['show_photo']
    readonly_fields = ['show_photo']
    list_editable = ['title']
    prepopulated_fields = {'slug': ['title']}

    @admin.display(description='Фотография')
    def show_photo(self, post: Post):
        if post.image:
            return mark_safe(f'<img src={post.image.url} width=50px height=50px>')
        else:
            return 'Нет фотографии'


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ['title']}


@admin.register(Tags)
class AdminTags(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    prepopulated_fields = {'slug': ['title']}