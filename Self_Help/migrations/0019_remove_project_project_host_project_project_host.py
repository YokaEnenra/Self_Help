# Generated by Django 4.1.4 on 2022-12-22 11:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Self_Help', '0018_project_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_host',
        ),
        migrations.AddField(
            model_name='project',
            name='project_host',
            field=models.ManyToManyField(related_name='host_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
