# Generated by Django 5.1.7 on 2025-04-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0019_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
