# Generated by Django 3.0.5 on 2020-04-28 10:32

import django.contrib.auth.validators
from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, default=users.models.random_icon_path, upload_to=users.models.User.get_image_path, verbose_name='アイコン'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.TextField(blank=True, max_length=140, null=True, verbose_name='自己紹介文'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=50, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='ユーザーネーム'),
        ),
    ]
