# Generated by Django 3.2.8 on 2021-11-01 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0007_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default=None, max_length=1024),
        ),
    ]
