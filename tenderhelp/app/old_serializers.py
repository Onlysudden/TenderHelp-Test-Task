import datetime
from rest_framework import serializers
import requests
import json

from .models import RegistryNumber

class RegistryGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegistryNumber
        fields = ('number', 'type', 'time', 'exists')

class RegistryCreateSerializer(serializers.ModelSerializer):
    
    type = serializers.SerializerMethodField(method_name='get_type', read_only=True)
    time = serializers.SerializerMethodField(method_name='get_time', read_only=True)
    exists = serializers.SerializerMethodField(method_name='get_exists', read_only=True)

    class Meta:
        model = RegistryNumber
        fields = ('number', 'type', 'time', 'exists')
    
    def get_type(self, obj):
        if len(str(obj.number)) == 10:
            return 'ИНН'
        else:
            return 'ОГРН'
    
    def get_time(self, obj):
        return datetime.datetime.now()

    def get_exists(self, obj):
        query = obj.number
        r = requests.post("https://rmsp.nalog.ru/search-proc.json", data={'query': query})
        d = json.loads(r.text)
        if d['data']:
            return True
        else:
            return False