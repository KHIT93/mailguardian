from .models import RuleDescription, Rule
from rest_framework import serializers

class RuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rule
        fields = ('id', 'url', 'name', 'score')

class RuleDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RuleDescription
        fields = ('id', 'url', 'key', 'value')
