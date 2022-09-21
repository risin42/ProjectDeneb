from argparse import Action
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import dbdata
from .serializers import dbdataSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly


class dbdataViewset(viewsets.ModelViewSet):
    """SQL平台数据库管理接口"""

    # 鉴权开关
    # authentication_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = dbdata.objects.all()
    # queryset = dbdata.objects.order_by('-id')[0]
    serializer_class = dbdataSerializer

    
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_dbdata(request):
    """SQL平台数据库管理接口"""
    if request.method == 'GET':
        lastDb = dbdata.objects.last()
        serializer = dbdataSerializer(lastDb)
        return Response(serializer.data)

