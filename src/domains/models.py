import uuid
from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save

# https://gist.github.com/solusipse/7ed8e1da104baaee3f05

# Create your models here.

# This maps to postfix virtual_mailbox_domains and virtual_transport
class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    destination = models.CharField(max_length=128, null=True, blank=True)
    relay_type = models.CharField(max_length=64, default='smtp')
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    catchall = models.BooleanField(default=False)
    # For commercial use in order to limit the number of recipient mailboxes that can be created
    allowed_accounts = models.IntegerField(default=-1)

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     self.relay_destination = self.relay_type + ':[' + self.destination + ']'
    #     super(Domain, self).save(*args, **kwargs)

# class Forwarder(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     source = models.CharField(max_length=80, unique=True)
#     destination = models.TextField()

class MailUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#    email = models.CharField(max_length=80, unique=True)
    domain = models.ForeignKey(Domain, related_name='domain', on_delete=models.CASCADE)
    is_domain_admin = models.BooleanField(default=False)
    user = models.OneToOneField(User, related_name='mailuser', on_delete=models.CASCADE)

    def __str__(self):
        return '{0} ({1} -> {2})'.format(self.user.email, self.domain, self.domain.destination)

# def create_mailuser(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         domain = Domain.objects.filter(name=user.email.split('@')[1]).first()
#         mail_user = MailUser(user=user, domain=domain.id)
#         mail_user.save()
# post_save.connect(create_mailuser, sender=User)

# class Transport(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     domain = models.CharField(max_length=128, unique=True)
#     transport = models.CharField(max_length=128)