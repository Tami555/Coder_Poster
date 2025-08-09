from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(pk=user_id)
            return user
        except user_model.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Проверяет, есть ли у пользователя указанное разрешение, не вызывая рекурсию.
        """
        if not user_obj.is_active:
            return False

        # Получаем queryset групп пользователя
        groups = user_obj.groups.all()

        # Проверяем, есть ли у какой-либо из групп пользователя нужное разрешение
        for group in groups:
            if group.permissions.filter(codename=perm.split('.')[-1],
                                         content_type__app_label=perm.split('.')[0]).exists():
                return True

        # Проверяем, есть ли у пользователя это разрешение напрямую
        return user_obj.user_permissions.filter(codename=perm.split('.')[-1],
                                              content_type__app_label=perm.split('.')[0]).exists()