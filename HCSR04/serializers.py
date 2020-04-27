from rest_framework_mongoengine import serializers

from .models import HCSR04


class HCSR04Serializer(serializers.DocumentSerializer):
    class Meta:
        model = HCSR04
        fields = '__all__'

