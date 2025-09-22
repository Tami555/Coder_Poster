from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coder, Subscription

admin.site.register(Coder, UserAdmin)
admin.site.register(Subscription, admin.ModelAdmin)