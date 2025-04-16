# Generated by Django 5.1.7 on 2025-04-16 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_account_rating_delete_rating'),
        ('property', '0016_property_creationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='associatedAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertys', to='account.account'),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
    ]
