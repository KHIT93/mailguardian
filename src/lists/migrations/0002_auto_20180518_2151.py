# Generated by Django 2.0.5 on 2018-05-18 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listentry',
            name='from_domain',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='From'),
        ),
        migrations.AddField(
            model_name='listentry',
            name='to_domain',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, verbose_name='To'),
        ),
    ]