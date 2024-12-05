from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Country
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    # Добавление стран
    if sender.name == "apps.visas": 
        countries = [
            {"name": "США"},
            {"name": "Канада"},
        ]
        for country in countries:
            Country.objects.get_or_create(name=country["name"])

    # Добавление группы для авторизации через Google (если нужно)
    if sender.name == "apps.auth":  # Пример для добавления в другое приложение
        group, created = Group.objects.get_or_create(name="GoogleAuthUsers")
        if created:
            permissions = Permission.objects.filter(codename__in=["add_user", "change_user"])
            group.permissions.set(permissions)
