# Generated by Django 4.2 on 2024-12-03 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visas', '0017_remove_visaorder_visa_type_visaorder_visa_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='visaorder',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Страна подачи'),
        ),
        migrations.AddField(
            model_name='visaorder',
            name='interview_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата собеседования'),
        ),
        migrations.AddField(
            model_name='visaorder',
            name='interview_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Время собеседования'),
        ),
    ]