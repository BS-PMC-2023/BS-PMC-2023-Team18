# Generated by Django 3.2.9 on 2022-01-02 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0008_alter_userprofileinfo_aboutme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='aboutme',
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='about',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
