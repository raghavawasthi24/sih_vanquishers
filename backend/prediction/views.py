from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from .serializers import *
from .detection import tree_count
class PredictionView(GenericAPIView):
    parser_classes=(MultiPartParser,)
    serializer_class=PredictionViewSerializer
    queryset=PredictionImages.objects.all()
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        b=serializer.data['image']
        # except:
        # b=0
        b=tree_count(b)
        return Response({"tree":b})