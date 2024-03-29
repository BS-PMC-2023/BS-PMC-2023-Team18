# Generated by Django 3.2.18 on 2023-05-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='city',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='facebook',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='gloves',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='google_location',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='market',
            name='hat',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='jacket',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='market_manager',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='other',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='pants',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='rating',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='market',
            name='scarf',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='shirt',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='shoes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='market',
            name='status',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
