# serializers.py
# 用户序列化
from rest_framework import serializers
from logic.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        # 要显示出来的字段
        fields = ('id', 'u_name', 'u_password')
