# Generated by Django 2.1.2 on 2018-10-20 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20181020_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='leader',
            field=models.CharField(default='', max_length=150),
        ),
    ]
