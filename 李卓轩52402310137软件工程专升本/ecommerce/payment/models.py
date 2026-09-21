from django.db import models
from orders.models import Order

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行转账'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待支付'),
        ('success', '支付成功'),
        ('failed', '支付失败'),
        ('refunded', '已退款'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', verbose_name='订单')
    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES, verbose_name='支付方式')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='支付金额')
    transaction_id = models.CharField(max_length=128, blank=True, verbose_name='交易流水号')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending', verbose_name='支付状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')
    refunded_at = models.DateTimeField(null=True, blank=True, verbose_name='退款时间')
    
    class Meta:
        verbose_name = '支付记录'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.get_payment_method_display()} - {self.order.order_number}'
