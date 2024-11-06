from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создает группы пользователей и назначает разрешения'

    def handle(self, *args, **options):
        # Создание групп
        super_admin_group, created = Group.objects.get_or_create(name='Супер Админ')
        employee_group, created = Group.objects.get_or_create(name='Сотрудник визового центра')
        client_group, created = Group.objects.get_or_create(name='Клиент')

        # Назначение прав для Супер Админа
        all_permissions = Permission.objects.all()
        super_admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS('Права для Супер Админа назначены'))

        # Назначение прав для Сотрудника визового центра
        # Даем доступ ко всем моделям, кроме пользователей и настроек
        employee_permissions = Permission.objects.exclude(content_type__app_label='auth').exclude(content_type__app_label='admin')
        employee_group.permissions.set(employee_permissions)
        self.stdout.write(self.style.SUCCESS('Права для Сотрудника визового центра назначены'))

        # Клиентам не назначаем права администрирования
        self.stdout.write(self.style.SUCCESS('Группа Клиент создана'))
