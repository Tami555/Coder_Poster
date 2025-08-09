"""
URL configuration for Coder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from django.views.decorators.cache import cache_page

from . import settings
from django.contrib.sitemaps.views import sitemap
from posts.sitemaps import PostsMap, CategoryMap, TagsMap

sitemaps = {'posts': PostsMap, 'category': CategoryMap, 'tags': TagsMap}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('users/', include('users.urls', namespace='users')),
    path("", include('social_django.urls', namespace="social")),
    path("sitemap.xml", cache_page(600)(sitemap), {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",)
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Админка Coder-Poster'