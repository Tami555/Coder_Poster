from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class GetPagesTestCase(TestCase):
    fixtures = ['fixtures/db.json']

    def test_get_all(self):
        posts = Post.objects.all().select_related('category').prefetch_related('tags').order_by('-data_update')
        path = reverse('all_posts')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], posts[:5])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_one_post(self):
        post = Post.objects.get(pk=1)

        path = reverse('post_by_slug', args=['pochemu-django-do-sih-por-ne-umer'])
        response = self.client.get(path)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('posts/one_post_page.html')
        self.assertEqual(response.context_data['post'], post)


class DostupTestCase(TestCase):
    def test_edit_not_your_post(self):
        pass

    def test_add_post_without_authentication(self):
        user = get_user_model().objects.create(username='Tobi')
        data = {
            'slug': 'ddd',
            'title': 'post1',
            'description': '111ddddd',
            'content': 'qwaszx',
            'image': '/posts_image/django-python.jpg',
            'data_create': datetime.now(),
            'data_update': datetime.now(),
            'category_id': 1,
            'coder_id': user.pk
        }
        path = reverse('add_post')
        response = self.client.post(path, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login') + '?next=' + path)





