# Generated by Django 3.2 on 2022-09-09 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0006_auto_20220909_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='slug',
        ),
    ]
