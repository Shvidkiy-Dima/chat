# Generated by Django 3.1.2 on 2020-10-04 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_user', '0007_auto_20201003_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_image'),
        ),
    ]
