from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

# функция для автоматического добавления нового пользователя в группу "Клиенты"
@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:  # Только для новых пользователей
        client_group, _ = Group.objects.get_or_create(name="Клиент")  # Проверяем или создаем группу
        instance.groups.add(client_group)  # Добавляем пользователя в группу
