# Generated by Django 3.2.4 on 2021-09-21 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='chat_id',
        ),
    ]
