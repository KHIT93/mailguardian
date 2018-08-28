from rest_framework import serializers

class MessagesByDateSerializer(serializers.Serializer):
    date = serializers.DateField()
    id__count = serializers.IntegerField()
    is_spam_count = serializers.IntegerField()
    size__sum = serializers.FloatField()
    infected_count = serializers.IntegerField()

class MessageRelaysSerializer(serializers.Serializer):
    client_ip = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    is_spam_count = serializers.IntegerField()
    size__sum = serializers.FloatField()
    infected_count = serializers.IntegerField()

class MessagesPerHourSerializer(serializers.Serializer):
    timestamp = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()

class TopSendersByQuantitySerializer(serializers.Serializer):
    from_address = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()

class TopSendersByVolumeSerializer(serializers.Serializer):
    from_address = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()

class TopRecipientsByQuantitySerializer(serializers.Serializer):
    to_address = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()

class TopRecipientsByVolumeSerializer(serializers.Serializer):
    to_address = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()

class TopSenderDomainsByQuantitySerializer(serializers.Serializer):
    from_domain = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()

class TopSenderDomainsByVolumeSerializer(serializers.Serializer):
    from_domain = serializers.CharField(max_length=255)
    size__sum = serializers.FloatField()

class TopRecipientDomainsByQuantitySerializer(serializers.Serializer):
    to_domain = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()

class TopRecipientDomainsByVolumeSerializer(serializers.Serializer):
    to_domain = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()
    size__sum = serializers.FloatField()