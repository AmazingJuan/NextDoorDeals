# Generated by Django 5.1.7 on 2025-04-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_account_creationdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='rating',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
