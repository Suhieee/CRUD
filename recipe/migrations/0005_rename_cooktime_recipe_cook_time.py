# Generated by Django 5.1.2 on 2024-10-27 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='cooktime',
            new_name='cook_time',
        ),
    ]