# Generated by Django 4.1.4 on 2022-12-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Self_Help', '0020_project_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]