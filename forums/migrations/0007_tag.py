# Generated by Django 3.2.8 on 2021-11-01 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0006_likecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
    ]
