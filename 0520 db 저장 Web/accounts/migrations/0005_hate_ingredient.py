# Generated by Django 3.2.5 on 2022-05-20 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_hate_ingredient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hate_Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('ingredients', models.TextField()),
            ],
        ),
    ]
