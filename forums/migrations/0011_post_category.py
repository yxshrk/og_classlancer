# Generated by Django 3.2.8 on 2021-11-01 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0010_remove_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(default=None, max_length=1024, null=True),
        ),
    ]
