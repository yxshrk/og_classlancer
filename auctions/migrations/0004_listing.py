# Generated by Django 3.2.4 on 2021-09-08 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.CharField(default=None, max_length=64, null=True)),
                ('teacher', models.CharField(default=None, max_length=64, null=True)),
                ('subject', models.CharField(default=None, max_length=100, null=True)),
                ('description', models.TextField(default=None, null=True)),
                ('price', models.CharField(default=None, max_length=64, null=True)),
                ('datetime', models.CharField(default=None, max_length=1024, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
