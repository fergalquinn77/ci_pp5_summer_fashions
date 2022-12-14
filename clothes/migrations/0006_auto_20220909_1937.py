# Generated by Django 3.2 on 2022-09-09 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0005_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='date_created',
            new_name='added_date',
        ),
        migrations.RenameField(
            model_name='wishlist',
            old_name='item',
            new_name='wished_item',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='last_updated',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='slug',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
