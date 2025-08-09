import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegistrationUserForm(UserCreationForm):
    this_year = datetime.date.today().year
    birthday = forms.DateField(required=False, label='День Рождения', widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'first_name', 'last_name', 'email',
                  'birthday', 'about', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким E-mail уже есть !')
        return email


class EditAccountUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин')
    email = forms.EmailField(disabled=True, label='E-mail')
    this_year = datetime.date.today().year
    birthday = forms.DateField(label='День Рождения',
                               widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year - 5))))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'photo', 'first_name', 'last_name',
                  'birthday', 'about']