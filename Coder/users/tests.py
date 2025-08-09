from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginCoderTestCase(TestCase):

    def setUp(self):
        self.new_user = {
            'username': 'user1Love',
            'first_name': 'Федя',
            'last_name': 'Воробьев',
            'email': 'vorobie@gmail.com',
            'about': 'ggggg',
            'password1': '12345qwertasdfg',
            'password2': '12345qwertasdfg',
        }

    def test_get_forma_registration(self):
        path = reverse('users:registration')
        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/forms.html')

    def test_registration_success(self):
        path = reverse('users:registration')
        response = self.client.post(path, self.new_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(get_user_model().objects.filter(username=self.new_user['username']).exists)

    def test_registration_double_user_error(self):
        get_user_model().objects.create(username=self.new_user['username'])
        # повторная регистрация того же пользователя
        path = reverse('users:registration')
        response = self.client.post(path, self.new_user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')



