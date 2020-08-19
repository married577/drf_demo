# 用户认证
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from logic.models import UserModel


class UserAuth(BaseAuthentication):
    # 验证user及token
    def authenticate(self, request):
        # 判断是否是get请求，其他请求直接可以访问
        if request.method == 'GET':
            # 从请求地址栏获取token（query_params)
            token = request.query_params.get('token')
            try:
                u_id = cache.get(token)
                user = UserModel.objects.get(pk=u_id)
                return user, token
            except:  # 若验证没成功返回None
                return
