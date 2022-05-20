# Generated by Django 3.2.5 on 2022-05-20 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_hate_ingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hate_ingredient',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='hate_ingredient',
            name='user_id',
        ),
        migrations.AddField(
            model_name='hate_ingredient',
            name='ingredient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.ingredient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hate_ingredient',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
