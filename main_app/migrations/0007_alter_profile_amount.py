# Generated by Django 5.0.3 on 2025-02-24 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_transfer_transaction_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
