# Generated by Django 5.1.7 on 2025-03-14 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='property',
            name='image',
        ),
        migrations.RemoveField(
            model_name='property',
            name='location',
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
        migrations.AlterField(
            model_name='property',
            name='propertyType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.propertytype'),
        ),
    ]
