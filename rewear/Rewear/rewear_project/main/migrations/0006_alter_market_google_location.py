# Generated by Django 3.2.18 on 2023-05-08 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_myevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='google_location',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
