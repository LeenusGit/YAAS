# Generated by Django 2.1.2 on 2018-10-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20181020_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='leader',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
