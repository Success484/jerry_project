# Generated by Django 5.0.3 on 2025-01-29 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pin',
            field=models.IntegerField(default=2002),
        ),
    ]
