# Generated by Django 2.1.2 on 2018-10-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='isBanned',
            field=models.BooleanField(default=False),
        ),
    ]