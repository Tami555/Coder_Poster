from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coder

admin.site.register(Coder, UserAdmin)
