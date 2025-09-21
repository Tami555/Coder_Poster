from django import forms
from .models import Post, Category, Tags


class AddPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Не выбрано')
    tags = forms.ModelMultipleChoiceField(queryset=Tags.objects.all(), label='Теги')

    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'content', 'category', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 5:
            raise forms.ValidationError("Можно выбрать не более 5 тегов.")
        return tags