# Generated by Django 5.0.3 on 2025-04-19 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_alter_chatbox_message_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbox',
            name='message',
            field=models.CharField(default=1, max_length=999),
            preserve_default=False,
        ),
    ]
