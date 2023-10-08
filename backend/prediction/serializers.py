from rest_framework import serializers
from .models import *
class PredictionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=PredictionImages
        fields=['id','image']
    