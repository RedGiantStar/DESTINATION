from django.db import models
from accounts.models import User
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username}的购物车'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='购物车')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    
    class Meta:
        verbose_name = '购物车商品'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity
