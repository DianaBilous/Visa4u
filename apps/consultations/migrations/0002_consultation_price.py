# Generated by Django 4.2 on 2024-10-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=7000, max_digits=10),
        ),
    ]