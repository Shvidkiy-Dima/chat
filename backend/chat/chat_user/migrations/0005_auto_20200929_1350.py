# Generated by Django 3.0.7 on 2020-09-29 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_user', '0004_auto_20200929_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='user_image/'),
        ),
    ]
