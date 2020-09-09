from rest_framework import serializers
from .models import DataLogEntry

class DataLogEntrySerializer(serializers.HyperlinkedModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    actor_email = serializers.SerializerMethodField()
    class Meta:
        model = DataLogEntry
        fields = (
            'id',
            'url',
            'content_type_name',
            'object_pk',
            'object_id',
            'object_repr',
            'action',
            'changes',
            'actor',
            'actor_email',
            'remote_addr',
            'timestamp',
            'additional_data',
        )

    def get_content_type_name(self, obj):
        return obj.content_type.__str__()
    
    def get_actor_email(self, obj):
        return obj.actor.email if obj.actor else None