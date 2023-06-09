# Generated by Django 4.2.1 on 2023-06-01 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('autopark', '0002_rename_vehicle_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_from', models.DateTimeField()),
                ('booking_to', models.DateTimeField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('approved', models.BooleanField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autopark.vehicle')),
            ],
        ),
    ]
