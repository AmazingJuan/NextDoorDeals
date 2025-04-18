# Generated by Django 5.1.7 on 2025-04-17 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_account_rating_delete_rating'),
        ('property', '0020_alter_visit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=280, null=True)),
                ('rate', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('reviewed_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='property.property')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
        ),
    ]
