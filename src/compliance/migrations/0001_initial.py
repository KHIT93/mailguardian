# Generated by Django 3.1.1 on 2020-09-07 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_pk', models.CharField(db_index=True, max_length=255, verbose_name='object pk')),
                ('object_id', models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='object id')),
                ('object_repr', models.TextField(verbose_name='object representation')),
                ('action', models.CharField(blank=True, choices=[('created', 'create'), ('updated', 'update'), ('deleted', 'delete')], max_length=32, null=True, verbose_name='action')),
                ('changes', models.TextField(blank=True, verbose_name='change message')),
                ('remote_addr', models.GenericIPAddressField(blank=True, null=True, verbose_name='remote address')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('additional_data', models.JSONField(blank=True, null=True, verbose_name='additional data')),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='actor')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.contenttype', verbose_name='content type')),
            ],
            options={
                'verbose_name': 'datalog entry',
                'verbose_name_plural': 'datalog entries',
                'ordering': ['-timestamp'],
                'get_latest_by': 'timestamp',
            },
        ),
    ]