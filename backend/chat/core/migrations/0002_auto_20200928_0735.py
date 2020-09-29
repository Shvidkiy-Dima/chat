# Generated by Django 3.0.7 on 2020-09-28 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialog',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='message',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='message',
            name='who_viewed_it',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dialog',
            name='users',
            field=models.ManyToManyField(related_name='dialogs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_msgs', to=settings.AUTH_USER_MODEL),
        ),
    ]
