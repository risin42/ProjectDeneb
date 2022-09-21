
from rest_framework import serializers
from .models import dbdata


class dbdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = dbdata
        fields = "__all__"
        # 控制 API 返回的字段
        # fields = ['id']
