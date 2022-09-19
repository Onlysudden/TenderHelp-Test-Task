from rest_framework import serializers

from .models import RegistryNumber

class RegistrySerializer(serializers.ModelSerializer):
    
    type = serializers.CharField(min_length=10, max_length=13, read_only=True)
    time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    exists = serializers.BooleanField(read_only=True)

    class Meta:
        model = RegistryNumber
        fields = ('number', 'type', 'time', 'exists')