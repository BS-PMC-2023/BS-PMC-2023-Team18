# Generated by Django 3.2.9 on 2022-01-02 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0010_alter_userprofileinfo_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='about',
            field=models.TextField(default='', max_length=400),
        ),
    ]
