# Generated by Django 2.0.6 on 2018-07-04 17:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180627_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailScannerHost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('hostname', models.CharField(max_length=255)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Address')),
                ('use_tls', models.BooleanField(default=True)),
            ],
        ),
    ]