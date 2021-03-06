# Generated by Django 3.0.5 on 2020-04-20 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=64)),
                ('description', models.TextField(default='')),
                ('content_type', models.CharField(choices=[('scratch', 'Scratch'), ('unity', 'Unity'), ('web', 'Web'), ('artwork3d', '3D Artwork'), ('artwork2d', '2D Artwork'), ('other', 'Other')], default='scratch', max_length=32)),
                ('image', models.ImageField(upload_to=main.models.Content.get_image_path)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
