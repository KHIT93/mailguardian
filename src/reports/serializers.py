from rest_framework import serializers

class MessagesByDateSerializer(serializers.Serializer):
    date = serializers.DateField()
    id__count = serializers.IntegerField()

class MessageRelaysSerializer(serializers.Serializer):
    client_ip = serializers.CharField(max_length=255)
    id__count = serializers.IntegerField()