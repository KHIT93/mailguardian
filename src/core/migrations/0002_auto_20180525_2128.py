# Generated by Django 2.0.5 on 2018-05-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='daily_quarantine_report',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='monthly_quarantine_report',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='weekly_quarantine_report',
            field=models.BooleanField(default=False),
        ),
    ]