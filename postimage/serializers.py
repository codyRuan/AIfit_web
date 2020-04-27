from rest_framework_mongoengine import serializers
from .models import postimage

class PostSerializer(serializers.DocumentSerializer):
    class Meta:
        model = postimage
        fields = '__all__'