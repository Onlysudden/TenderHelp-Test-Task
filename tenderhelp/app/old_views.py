from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RegistryNumber
from .serializers import RegistryCreateSerializer, RegistryGetSerializer

class RegistryAPIView(APIView):
    serializer_class = RegistryCreateSerializer

    def get_queryset(self):
        numbers = RegistryNumber.objects.all()
        return numbers
    
    # def get_serializer_class(self, request):
    #     if self.request.method is 'GET':
    #         return RegistryGetSerializer
    #     elif self.request.method is 'POST':
    #         return RegistryCreateSerializer
    #     else:
    #         return Response({'Invalid': 'Method not allowed'})

    def get(self, request):
        numbers = self.get_queryset()
        serializer = RegistryGetSerializer(numbers, many=True)
        return Response({'get': serializer.data})
    
    def post(self, request):
        serializer = RegistryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})
    
    def delete(self, request):
        all_numbers = RegistryNumber.objects.all()

        if all_numbers:
            all_numbers.delete()
            return Response({'delete': 'delete all'})
        return Response({'delete': 'data is clean'})