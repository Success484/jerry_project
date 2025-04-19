# Generated by Django 5.0.3 on 2025-04-19 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_transfer_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbox',
            name='message_image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images'),
        ),
        migrations.AlterField(
            model_name='chatbox',
            name='message',
            field=models.CharField(blank=True, max_length=999, null=True),
        ),
    ]
