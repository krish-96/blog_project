# Generated by Django 3.0.5 on 2020-04-18 10:28

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, max_length=264, unique=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('name', 'slug')},
        ),
    ]
