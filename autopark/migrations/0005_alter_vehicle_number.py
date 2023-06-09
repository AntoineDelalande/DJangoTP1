# Generated by Django 4.2.1 on 2023-06-07 16:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopark', '0004_alter_vehicle_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='number',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(message="Ce champ ne correspond pas aux formats des plaques d'immatriculation francaises", regex='^[A-Z]{2}-[0-9]{3}-[A-Z]{2}|^[0-9]{4}[A-Z]{2}[0-9]{2}$')]),
        ),
    ]
