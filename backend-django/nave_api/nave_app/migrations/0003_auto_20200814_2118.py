# Generated by Django 3.1 on 2020-08-14 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nave_app', '0002_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]