# Generated by Django 2.0 on 2018-01-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0008_auto_20180106_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_mcp',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='released',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='size',
            field=models.FloatField(default=0),
        ),
    ]
