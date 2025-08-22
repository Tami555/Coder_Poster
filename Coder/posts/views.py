from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch, Q
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from posts.models import Post, Tags, Category
from .forms import AddPostForm
from users.utils import DataFormMixin


def main_page(request: HttpRequest):
    return HttpResponse('Главная страница')


class AllPosts(ListView):
    template_name = 'posts/posts_page.html'
    extra_context = {'title': 'Поостыыы'}
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags').order_by('-data_update')


class PostsBySearch(ListView):
    template_name = 'posts/posts_page.html'
    context_object_name = 'posts'
    search = ''

    def get_queryset(self):
        self.search = self.kwargs['search']
        return Post.objects.filter(Q(title__icontains=self.search) | Q(description__icontains=self.search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты | {self.search}'
        context['title_type'] = self.search
        return context


class PostsByTag(ListView):
    template_name = 'posts/posts_page.html'
    context_object_name = 'posts'
    tag_title = ''
    paginate_by = 5

    def get_queryset(self):
        tag = Tags.objects.get(slug=self.kwargs['slug_tag'])
        self.tag_title = tag.title
        return tag.posts.all().select_related('category', 'coder').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты & {self.tag_title}'
        context['title_type'] = self.tag_title
        return context


class PostsByCategory(ListView):
    template_name = 'posts/posts_page.html'
    context_object_name = 'posts'
    category_title = ''
    paginate_by = 5

    def get_queryset(self):
        cat = Category.objects.get(slug=self.kwargs['slug_category'])
        self.category_title = cat.title
        return cat.posts.all().select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Посты & {self.category_title}'
        context['title_type'] = self.category_title
        return context


class OnePost(DetailView):
    template_name = 'posts/one_post_page.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug_post'

    def get_object(self, queryset=None):
        post = Post.objects.filter(
            slug=self.kwargs['slug_post']
        ).select_related('category', 'coder').prefetch_related(Prefetch('tags', queryset=Tags.objects.only('title', 'slug'))).first()

        if not post:
            raise Http404("Post not found")
        return post


class AddPost(DataFormMixin, PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'users/forms.html'
    title_page = 'Создать свой пост'
    btn_title = 'Сохранить'
    permission_required = 'posts.add_post'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('all_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.coder = self.request.user
        return super().form_valid(form)


class EditPost(DataFormMixin, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    # model = Post
    # fields = ['title', 'description', 'image', 'content', 'category', 'tags']
    form_class = AddPostForm
    template_name = 'users/forms.html'
    slug_url_kwarg = 'slug_post'
    title_page = 'Редактировать пост'
    btn_title = 'Сохранить изменения'
    login_url = 'users:login'
    permission_required = 'posts.change_post'

    def get_object(self, queryset=None):
        post = Post.objects.get(slug=self.kwargs['slug_post'])
        if post:
            if post.coder == self.request.user:
                return post
            else:
                raise PermissionDenied()
        else:
            raise Http404('Такой пост не найден !')

    def get_success_url(self):
        # return reverse('users:profile', args=self.request.user.pk)
        return reverse('all_posts')


class DeletePost(DataFormMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'users/forms.html'
    slug_url_kwarg = 'slug_post'
    title_page = 'Удалить пост'
    btn_title = 'Удалить'
    login_url = 'users:login'
    permission_required = 'posts.delete_post'

    def get_object(self, queryset=None):
        post = Post.objects.get(slug=self.kwargs['slug_post'])
        if post:
            if post.coder == self.request.user:
                return post
            else:
                raise PermissionDenied()
        else:
            raise Http404('Такой пост не найден !')

    def get_success_url(self):
        return reverse('users:profile', args=[self.request.user.pk])


def error_404(request: HttpRequest, exception):
    context = {
        'status_code': '404 Not Found',
        'error_message': 'Ничего не найдено!!',
        'error_image': 'images/er404.png',
        'error_description': 'Эта страница пока не существует... Еще. Может быть, она появится в следующем релизе. А пока, вернитесь на главную'
    }
    return HttpResponseNotFound(render(request, 'errors.html', context).content)


def error_403(request: HttpRequest, exception):
    context = {
        'status_code': '🚫 403 Forbidden️',
        'error_message': 'Ты не пройдёшь! 🧙‍♂️',
        'error_image': 'images/er403.png',
        'error_description': 'У вас нет прав доступа к этой секретной зоне. Вернитесь туда, где вас ждут (на главную страницу)'
    }
    return HttpResponseForbidden(render(request, 'errors.html', context).content)


def error_413(request: HttpRequest, exception):
    context = {
        'status_code': '🐘 413 Payload Too Large',
        'error_message': 'Ого, ты что, целый Docker-образ залил?!️',
        'error_image': 'images/er413.png',
        'error_description': "Твой запрос весит больше, чем документация к PHP.\n Попробуй ужать его, как node_modules в продакшене."
    }
    return HttpResponse(render(request, 'errors.html', context).content, status=413)


def error_500(request: HttpRequest):
    context = {
        'status_code': '500 Internal Server Error',
        'error_message': "Сервер ушёл в бесконечный цикл раздумий 🤖💭",
        'error_image': 'images/er500.png',
        'error_description': "Мы уже разбираемся — как обычно, это был кривой запрос к БД.\nПопей кофе ☕, мы скоро всё починим (нет)."
    }
    return HttpResponseServerError(render(request, 'errors.html', context).content)