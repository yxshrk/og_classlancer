# Generated by Django 3.2.4 on 2021-10-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_auto_20211003_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeslots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listingid', models.IntegerField()),
                ('timeslot', models.CharField(default=None, max_length=1024, null=True)),
                ('selected', models.BooleanField(default=None)),
            ],
        ),
    ]
