# Generated by Django 2.1.4 on 2019-01-02 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20181106_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listentry',
            name='from_address',
            field=models.CharField(db_index=True, default='', max_length=511, verbose_name='From'),
        ),
        migrations.AlterField(
            model_name='listentry',
            name='to_address',
            field=models.CharField(db_index=True, default='', max_length=511, verbose_name='To'),
        ),
    ]
