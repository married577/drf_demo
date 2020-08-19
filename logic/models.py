# models.py
from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=32, unique=True)  # 用户名唯一
    # 密码需要加密，加密后比较长
    u_password = models.CharField(max_length=256)
