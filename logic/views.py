# views.py
from django.core.cache import cache
# 创建用户（用户的注册和登录），（超级管理员）查询用户

# 创建用户
import uuid
from rest_framework import status, exceptions, mixins, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
# ListCreateAPIView:可以用于用户的创建和查询
from rest_framework.response import Response
from logic.auth import UserAuth
from logic.models import UserModel
from logic.serializers import UserSerializer


class UsersViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    # 序列化类
    serializer_class = UserSerializer
    # 查询集和结果集
    queryset = UserModel.objects.all()
    # 用户验证
    authentication_classes = (UserAuth,)

    # 同一个post做把登录和注册同时完成
    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')
        # 若参数为register则为注册，创建用户
        if action == 'login':
            return self.create(request, *args, **kwargs)
        elif action == 'register':
            # 验证用户名密码
            u_name = request.data.get('u_name')
            u_password = request.data.get('u_password')
            try:
                user = UserModel.objects.get(u_name=u_name)   # 数据库验证用户名
                # 用户名存在验证密码
                if user.u_password == u_password:
                    # 生成令牌,传入客户端和放入服务器缓存或者数据库
                    token = uuid.uuid4().hex
                    # 把token放入缓存,注意Redis在settings中的配置
                    cache.set(token, user.id)
                    # 并传入客户端
                    data = {
                        'msg': 'ok',
                        'status': 200,
                        'token': token
                    }
                    return Response(data)
                else:
                    raise exceptions.AuthenticationFailed   # 用户密码错误
            except UserModel.DoesNotExist:
                raise exceptions.NotFound   # 用户名错误
        else:
            raise exceptions.ValidationError  # 验证错误，传入的不是POST请求


# 单个用户,只用于展示
class UserAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
