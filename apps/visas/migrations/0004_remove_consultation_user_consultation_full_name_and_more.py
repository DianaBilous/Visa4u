# Generated by Django 4.2 on 2024-10-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visas', '0003_consultation_assigned_manager_consultation_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='user',
        ),
        migrations.AddField(
            model_name='consultation',
            name='full_name',
            field=models.CharField(default='Unknown', max_length=255, verbose_name='ФИО'),
        ),
        migrations.AddField(
            model_name='visaorder',
            name='required_documents',
            field=models.ManyToManyField(blank=True, to='visas.visadocument'),
        ),
        migrations.AlterField(
            model_name='visaorder',
            name='status',
            field=models.CharField(choices=[('paid', 'Заказ оплачен'), ('manager_assigned', 'Менеджер назначен'), ('awaiting_documents', 'Ожидание документов'), ('awaiting_interview', 'Ожидание записи'), ('scheduled', 'Записан на собеседование'), ('approved', 'Виза одобрена'), ('denied', 'Отказ'), ('completed', 'Заявка закрыта')], default='paid', max_length=20, verbose_name='Статус заказа'),
        ),
    ]
