# Generated by Django 2.0 on 2018-01-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0016_auto_20180110_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.TextField(blank=True, db_index=True, default=''),
        ),
    ]
