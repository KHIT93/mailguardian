# Generated by Django 3.0.9 on 2020-08-07 17:41

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_mailscannerhost_passive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twofactorbackupcode',
            name='code',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=255, verbose_name='Two Factor Backup Code')),
        ),
        migrations.AlterField(
            model_name='twofactorconfiguration',
            name='totp_key',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=255, verbose_name='Timebased Onetime Password Key')),
        ),
    ]