# Generated by Django 2.0.5 on 2018-05-15 10:53

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Headers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MailscannerReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='McpReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_address', models.CharField(blank=True, db_index=True, default='', max_length=511, verbose_name='From')),
                ('from_domain', models.CharField(blank=True, db_index=True, default='', max_length=255)),
                ('to_address', models.CharField(blank=True, db_index=True, default='', max_length=511, verbose_name='To')),
                ('to_domain', models.CharField(blank=True, db_index=True, default='', max_length=255)),
                ('subject', models.TextField(blank=True, db_index=True, default='')),
                ('client_ip', models.GenericIPAddressField(db_index=True, null=True, verbose_name='Client IP')),
                ('mailscanner_hostname', models.CharField(db_index=True, max_length=255)),
                ('spam_score', models.DecimalField(db_index=True, decimal_places=2, default=0.0, max_digits=7)),
                ('mcp_score', models.DecimalField(blank=True, db_index=True, decimal_places=2, default=0.0, max_digits=7, null=True)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('date', models.DateField(db_index=True)),
                ('size', models.FloatField(default=0)),
                ('token', models.CharField(max_length=255, null=True)),
                ('mailq_id', models.TextField(null=True, verbose_name='Mailqueue identification')),
                ('whitelisted', models.BooleanField(db_index=True, default=False)),
                ('blacklisted', models.BooleanField(db_index=True, default=False)),
                ('is_spam', models.BooleanField(db_index=True, default=False)),
                ('is_mcp', models.BooleanField(db_index=True, default=False)),
                ('is_rbl_listed', models.BooleanField(db_index=True, default=False, verbose_name='Is RBL listed')),
                ('quarantined', models.BooleanField(db_index=True, default=False)),
                ('infected', models.BooleanField(db_index=True, default=False)),
                ('released', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'ordering': ('-timestamp',),
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='RblReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField(blank=True, null=True)),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mail.Message')),
            ],
        ),
        migrations.CreateModel(
            name='SpamAssassinRule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpamReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contents', models.TextField(blank=True, null=True)),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mail.Message')),
            ],
        ),
        migrations.CreateModel(
            name='TransportLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('transport_host', models.CharField(db_index=True, max_length=255)),
                ('transport_type', models.CharField(db_index=True, max_length=255)),
                ('relay_host', models.CharField(db_index=True, max_length=255)),
                ('dsn', models.CharField(db_index=True, max_length=255)),
                ('dsn_message', models.TextField(db_index=True)),
                ('delay', models.DurationField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mail.Message')),
            ],
            options={
                'ordering': ('timestamp',),
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'from_domain'], name='mail_messag_from_ad_73cd6c_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'to_domain'], name='mail_messag_to_addr_0cd3ce_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'to_address'], name='mail_messag_from_ad_f1acb9_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'to_domain'], name='mail_messag_from_ad_5833fe_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'from_domain'], name='mail_messag_to_addr_06c9aa_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'mailscanner_hostname'], name='mail_messag_client__f7ba93_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'blacklisted'], name='mail_messag_from_ad_676957_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'whitelisted'], name='mail_messag_from_ad_238390_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'infected'], name='mail_messag_from_ad_1f0d67_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'is_spam'], name='mail_messag_from_ad_12e43e_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'quarantined'], name='mail_messag_from_ad_2d4929_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_address', 'is_rbl_listed'], name='mail_messag_from_ad_2b9f87_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'blacklisted'], name='mail_messag_to_addr_eec52d_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'whitelisted'], name='mail_messag_to_addr_0f2921_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'infected'], name='mail_messag_to_addr_a7125d_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'is_spam'], name='mail_messag_to_addr_5cae52_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'quarantined'], name='mail_messag_to_addr_11d06f_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_address', 'is_rbl_listed'], name='mail_messag_to_addr_1e8598_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'blacklisted'], name='mail_messag_from_do_bf466c_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'whitelisted'], name='mail_messag_from_do_be122b_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'infected'], name='mail_messag_from_do_4a62bf_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'is_spam'], name='mail_messag_from_do_3d2668_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'quarantined'], name='mail_messag_from_do_e2e93e_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['from_domain', 'is_rbl_listed'], name='mail_messag_from_do_d8e7ed_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'blacklisted'], name='mail_messag_to_doma_48b624_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'whitelisted'], name='mail_messag_to_doma_da63ed_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'infected'], name='mail_messag_to_doma_e640e6_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'is_spam'], name='mail_messag_to_doma_752e4f_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'quarantined'], name='mail_messag_to_doma_1647b6_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['to_domain', 'is_rbl_listed'], name='mail_messag_to_doma_729d90_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'blacklisted'], name='mail_messag_client__31eae6_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'whitelisted'], name='mail_messag_client__9d8977_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'infected'], name='mail_messag_client__1577f4_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'is_spam'], name='mail_messag_client__ef32e1_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'quarantined'], name='mail_messag_client__0c4c11_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['client_ip', 'is_rbl_listed'], name='mail_messag_client__961a40_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'blacklisted'], name='mail_messag_mailsca_eec5db_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'whitelisted'], name='mail_messag_mailsca_e7750e_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'infected'], name='mail_messag_mailsca_9bc8e2_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'is_spam'], name='mail_messag_mailsca_04192b_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'quarantined'], name='mail_messag_mailsca_75aba8_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['mailscanner_hostname', 'is_rbl_listed'], name='mail_messag_mailsca_7437e6_idx'),
        ),
        migrations.AddField(
            model_name='mcpreport',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mail.Message'),
        ),
        migrations.AddField(
            model_name='mailscannerreport',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mail.Message'),
        ),
        migrations.AddField(
            model_name='headers',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mail.Message'),
        ),
    ]