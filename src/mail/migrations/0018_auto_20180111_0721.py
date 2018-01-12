# Generated by Django 2.0 on 2018-01-11 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0017_auto_20180110_0726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AddField(
            model_name='message',
            name='mcp_score',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='message',
            name='spam_score',
            field=models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=7),
        ),
    ]
