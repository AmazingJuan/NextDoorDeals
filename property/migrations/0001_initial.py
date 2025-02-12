# Generated by Django 5.1.6 on 2025-02-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('propertyType', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('location', models.URLField()),
                ('socioEconomicStatus', models.CharField(max_length=1)),
            ],
        ),
    ]
