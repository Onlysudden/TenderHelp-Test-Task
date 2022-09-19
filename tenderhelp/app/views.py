from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timezone
import requests
import json

from .models import RegistryNumber
from .serializers import RegistrySerializer

class RegistryAPIView(APIView):
    serializer_class = RegistrySerializer

    def get_queryset(self):
        numbers = RegistryNumber.objects.all()
        return numbers

    def get(self, request):
        numbers = self.get_queryset().order_by('-time')
        serializer = RegistrySerializer(numbers, many=True)
        return Response({"get": serializer.data})
    
    def post(self, request):
        request_data = request.data
        number = request_data['number']
        quantity = len(str(number))

        if quantity == 10 or quantity == 13:
            old_number = RegistryNumber.objects.filter(number=number).last()
            type = self._get_type(request=request_data)
            time = self._get_time(request)
            exists = self._get_exists(request)
            
            old_time = old_number.time
            delta_time = time - old_time

            if old_number and delta_time.seconds <= 300:
                serializer = RegistrySerializer(old_number)
                return Response({"old post": serializer.data})

            new_number = RegistryNumber.objects.create(number=number, type=type, time=time, exists=exists)
            new_number.save()

            serializer = RegistrySerializer(new_number)

            return Response({"post": serializer.data})
        else:
            return Response({"error": "The number should be 10 or 13 characters"})

    def _get_type(self, request):
        number = request['number']

        if len(str(number)) == 10:
            return 'ИНН'
        else:
            return 'ОГРН'
    
    def _get_time(self, request):
        return datetime.now(timezone.utc)

    def _get_exists(self, request):
        query = request.data['number']
        r = requests.post("https://rmsp.nalog.ru/search-proc.json", data={'query': query})
        d = json.loads(r.text)
        if d['data']:
            return True
        else:
            return False

"""     Добавил delete чтобы чистить базу

    def delete(self, request):
        all_numbers = RegistryNumber.objects.all()

        if all_numbers:
            all_numbers.delete()
            return Response({'delete': 'delete all'})
        return Response({'delete': 'data is clean'})
"""