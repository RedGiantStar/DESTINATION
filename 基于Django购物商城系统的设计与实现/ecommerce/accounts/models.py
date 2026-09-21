from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_login = models.DateTimeField(auto_now=True, verbose_name='最后登录时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    name = models.CharField(max_length=32, verbose_name='收货人姓名')
    phone = models.CharField(max_length=20, verbose_name='收货人手机号')
    province = models.CharField(max_length=32, verbose_name='省份')
    city = models.CharField(max_length=32, verbose_name='城市')
    district = models.CharField(max_length=32, verbose_name='区县')
    detail = models.CharField(max_length=256, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='是否默认地址')
    
    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.province}{self.city}{self.district}{self.detail}'
