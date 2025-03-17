# Generated by Django 5.1.7 on 2025-03-15 22:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0009_alter_images_image_alter_images_property'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='provinID',
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
    ]
