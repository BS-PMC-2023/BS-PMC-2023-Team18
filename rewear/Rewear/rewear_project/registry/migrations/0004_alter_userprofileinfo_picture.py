# Generated by Django 3.2.9 on 2021-12-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0003_userprofileinfo_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='picture',
            field=models.ImageField(blank=True, upload_to='static\\media\\profile_pics'),
        ),
    ]
