# Generated by Django 2.1.2 on 2018-10-12 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_isbanned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='isBanned',
        ),
        migrations.AddField(
            model_name='auction',
            name='state',
            field=models.CharField(choices=[(0, 'Active'), (1, 'Banned'), (2, 'Due'), (3, 'Adjudicated')], default='Active', max_length=10),
        ),
    ]
