# Generated by Django 5.1.7 on 2025-03-13 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_personaccount_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaccount',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.role'),
        ),
    ]
