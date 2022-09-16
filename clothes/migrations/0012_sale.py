# Generated by Django 3.2.15 on 2022-09-16 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothes', '0011_clothes_on_sale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_off', models.DecimalField(decimal_places=0, max_digits=2)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('clothes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clothes.clothes')),
            ],
        ),
    ]
