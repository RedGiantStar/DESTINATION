from django.db import models
from accounts.models import User, Address
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='收货地址')
    order_number = models.CharField(max_length=32, unique=True, verbose_name='订单号')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending', verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    payment_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    shipping_time = models.DateTimeField(null=True, blank=True, verbose_name='发货时间')
    completed_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'订单 {self.order_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='商品')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='小计')
    
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
