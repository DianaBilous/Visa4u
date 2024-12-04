# Generated by Django 4.2 on 2024-12-02 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visas', '0009_alter_visaorder_options_alter_country_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='documentupload',
            options={'verbose_name': 'Документ', 'verbose_name_plural': 'Загруженные документы'},
        ),
        migrations.AlterModelOptions(
            name='faq',
            options={'verbose_name': 'Часто задаваемый вопрос', 'verbose_name_plural': 'Часто задаваемые вопросы'},
        ),
        migrations.AlterModelOptions(
            name='visaassessment',
            options={'verbose_name': 'Запрос на бесплатную оценку шансов', 'verbose_name_plural': 'Запросы на бесплатную оценку шансов'},
        ),
        migrations.AlterModelOptions(
            name='visadocument',
            options={'verbose_name': 'Документ для визы', 'verbose_name_plural': 'Документы для виз'},
        ),
        migrations.AlterModelOptions(
            name='visarequirement',
            options={'verbose_name': 'Требование для визы', 'verbose_name_plural': 'Требования для виз'},
        ),
        migrations.AlterModelOptions(
            name='visatype',
            options={'verbose_name': 'Тип визы', 'verbose_name_plural': 'Типы виз'},
        ),
    ]