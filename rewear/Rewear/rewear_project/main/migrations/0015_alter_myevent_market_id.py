# Generated by Django 3.2.18 on 2023-05-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20230524_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myevent',
            name='market_id',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
    ]
