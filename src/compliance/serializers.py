from rest_framework import serializers
from .models import DataLogEntry

class DataLogEntrySerializer(serializers.HyperlinkedModelSerializer):
    content_type_name = serializers.SerializerMethodField()
    class Meta:
        model = DataLogEntry
        fields = (
            'content_type_name',
            'object_pk',
            'object_id',
            'object_repr',
            'action',
            'changes',
            'actor',
            'remote_addr',
            'timestamp',
            'additional_data',
        )

    def get_content_type_name(self, obj):
        return obj.content_type.__str__()