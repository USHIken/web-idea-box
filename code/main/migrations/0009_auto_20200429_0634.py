# Generated by Django 3.0.5 on 2020-04-29 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0008_contentvisit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentvisit',
            name='visitor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visits', to=settings.AUTH_USER_MODEL),
        ),
    ]
