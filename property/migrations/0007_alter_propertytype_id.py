# Generated by Django 5.1.7 on 2025-03-14 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_rename_name_property_title_alter_images_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertytype',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
