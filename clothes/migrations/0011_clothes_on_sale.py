# Generated by Django 3.2.15 on 2022-09-16 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0010_itemreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='on_sale',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]