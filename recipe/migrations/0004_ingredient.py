# Generated by Django 5.1.2 on 2024-10-26 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_instruction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=100)),
                ('metric', models.CharField(choices=[('GRAMS', 'GRAMS'), ('KILOGRAMS', 'KILOGRAMS'), ('MILLILITERS', 'MILLILITERS'), ('LITERS', 'LITERS'), ('TEASPOONS', 'TEASPOONS'), ('TABLESPOONS', 'TABLESPOONS'), ('CUPS', 'CUPS'), ('OUNCES', 'OUNCES'), ('POUNDS', 'POUNDS'), ('PIECES', 'PIECES'), ('NOT SPECIFIED', 'NOT SPECIFIED')], default='NOT SPECIFIED', max_length=20)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipe.recipe')),
            ],
        ),
    ]