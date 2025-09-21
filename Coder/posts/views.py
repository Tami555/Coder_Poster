import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch, Q
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseForbidden, HttpResponseNotFound, \
    HttpResponseServerError, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from posts.models import Post, Tags, Category, Reaction
from .forms import AddPostForm
from users.utils import DataFormMixin
# задачи celery
from .tasks import check_correct_post


def main_page(request: HttpRequest):
    return HttpResponse('Главная страница')


class AllPosts(ListView):
    template_name = 'posts/posts_page.html'
    extra_context = {'title': 'Поостыыы'}
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(Q(coder_id=self.request.user.id) | Q(status=Post.Status.APPROVED)).select_related(
            'category').prefetch_related('tags').order_by('-data_update')


class PostsBySearch(ListView):
    template_name = 'posts/posts_page.html'
    context_object_name = 'posts'
    search = ''

    def get_queryset(self):
        self.search = self.kwargs['search']
        return Post.objects.filter((Q(title__icontains=self.search) | Q(description__icontains=self.search))
                                   & Q(status=Post.Status.APPROVED))

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
        return tag.posts.filter(status=Post.Status.APPROVED).select_related('category', 'coder').prefetch_related('tags')

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
        return cat.posts.filter(status=Post.Status.APPROVED).select_related('category').prefetch_related('tags')

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
        post = Post.objects.filter(slug=self.kwargs['slug_post']
        ).select_related('category', 'coder').prefetch_related(Prefetch('tags', queryset=Tags.objects.only('title', 'slug'))).first()

        if not post or (post.status != Post.Status.APPROVED and post.coder_id != self.request.user.pk):
            raise Http404("Post not found")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']

        # Получаем реакцию текущего пользователя
        user_reaction = None
        if self.request.user.is_authenticated:
            user_reaction = post.get_user_reaction(self.request.user)

        context['user_reaction'] = user_reaction
        return context


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
        post.save()
        check_correct_post.apply_async((post.pk, post.title, post.description, post.content), countdown=10)
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
            if post.coder == self.request.user and post.status != Post.Status.CHECK:
                return post
            else:
                raise PermissionDenied()
        else:
            raise Http404('Такой пост не найден !')

    def get_success_url(self):
        # return reverse('users:profile', args=self.request.user.pk)
        return reverse('all_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Добавляем информацию о блокировке в контекст
        if post.status == Post.Status.BLOCKED:
            context['block_reason'] = post.moderator_comment
            context['is_blocked'] = True
        return self.get_context_mixin(context)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.status = Post.Status.CHECK
        post.moderator_comment = ''
        post.save()
        check_correct_post.apply_async((post.pk, post.title, post.description, post.content), countdown=10)
        return super().form_valid(form)


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
            if post.coder == self.request.user and post.status != Post.Status.CHECK:
                return post
            else:
                raise PermissionDenied()
        else:
            raise Http404('Такой пост не найден !')

    def get_success_url(self):
        return reverse('users:profile', args=[self.request.user.pk])


class LikeMePosts(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'posts/posts_page.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user_posts = self.request.user.post_reactions.values('post',).filter(
            reaction_type=Reaction.ReactionType.LIKE)
        posts = Post.objects.filter(pk__in=(x['post'] for x in user_posts), status=Post.Status.APPROVED)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Понравившиеся Посты'
        context['title_type'] = 'Мне Нравятся'
        return context


# Реакции на посты (лайки\дизлайки)
@require_http_methods(["POST"])
def set_reaction(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    try:
        # Для отладки сначала проверяем базовые вещи
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Требуется авторизация'
            }, status=401)

        data = json.loads(request.body)
        post_id = data.get('post_id')
        reaction_type = data.get('reaction_type')

        print(f"Received data: post_id={post_id}, reaction_type={reaction_type}")

        post = Post.objects.get(id=post_id)

        # Преобразуем строку в числовое значение
        reaction_value = 1 if reaction_type == 'like' else 0

        # Создаем или обновляем реакцию
        reaction, created = Reaction.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={'reaction_type': reaction_value}
        )

        return JsonResponse({
            'success': True,
            'message': 'Реакция сохранена!',
            'likes_count': post.get_likes_count(),
            'dislikes_count': post.get_dislikes_count(),
            'is_new': created
        })

    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Пост не найден'
        }, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Ошибка сервера'
        }, status=500)


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