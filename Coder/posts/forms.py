from django import forms
from .models import Post, Category, Tags


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Не выбрано')
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), label='Теги')

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'content', 'category', 'tags']
