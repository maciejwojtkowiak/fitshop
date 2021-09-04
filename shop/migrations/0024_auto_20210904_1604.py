# Generated by Django 3.2.6 on 2021-09-04 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_auto_20210830_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_currency',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price_currency',
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
