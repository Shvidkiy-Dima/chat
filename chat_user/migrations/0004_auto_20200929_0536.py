# Generated by Django 3.0.7 on 2020-09-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_user', '0003_auto_20200928_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='image',
            field=models.ImageField(blank=True, default='default.jpeg', null=True, upload_to='user_image/'),
        ),
    ]