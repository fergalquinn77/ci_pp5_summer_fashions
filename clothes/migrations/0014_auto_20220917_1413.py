# Generated by Django 3.2.15 on 2022-09-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0013_alter_sale_clothes'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='sale',
            name='percent_off',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
