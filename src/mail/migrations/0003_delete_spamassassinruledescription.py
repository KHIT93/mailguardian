# Generated by Django 2.0.7 on 2018-07-09 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20180709_1543'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SpamAssassinRuleDescription',
        ),
    ]
