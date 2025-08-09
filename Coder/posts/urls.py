from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
urlpatterns = [
    path('home-page/', views.main_page, name='home'),
    path('', views.AllPosts.as_view(), name='all_posts'),
    path('posts', cache_page(200)(views.AllPosts.as_view()), name='posts'),
    path('posts/tags/<slug:slug_tag>', views.PostsByTag.as_view(), name='post_by_tags'),
    path('posts/category/<slug:slug_category>', views.PostsByCategory.as_view(), name='post_by_category'),
    path('posts/<slug:slug_post>/', views.OnePost.as_view(), name='post_by_slug'),
    path('post/add/', views.AddPost.as_view(), name='add_post'),
    path('post/edit/<slug:slug_post>', views.EditPost.as_view(), name='edit_post'),
    path('post/delete/<slug:slug_post>', views.DeletePost.as_view(), name='delete_post'),
]