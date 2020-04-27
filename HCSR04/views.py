from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import HCSR04
from .serializers import HCSR04Serializer


class HCSR04View(APIView):

    def get(self, request):
        serializer = HCSR04Serializer(HCSR04.objects.all(), many=True)
        response = {"HCSR04": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data
        serializer = HCSR04Serializer(data=data)
        if serializer.is_valid():
            hcsr = HCSR04(**data)
            hcsr.save()
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)

# Create your views here.
