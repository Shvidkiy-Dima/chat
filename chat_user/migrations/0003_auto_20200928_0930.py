# Generated by Django 3.0.7 on 2020-09-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_user', '0002_chatuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_image/'),
        ),
    ]