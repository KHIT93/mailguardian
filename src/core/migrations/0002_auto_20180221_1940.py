# Generated by Django 2.0.2 on 2018-02-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailscannerconfiguration',
            name='filepath',
            field=models.CharField(default='/etc/MailScanner/MailScanner.conf', max_length=511),
        ),
        migrations.AlterField(
            model_name='mailscannerconfiguration',
            name='value',
            field=models.TextField(),
        ),
    ]
