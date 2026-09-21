from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='分类名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='父分类')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='商品名称')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='所属分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(default=0, verbose_name='库存')
    description = models.TextField(blank=True, verbose_name='商品描述')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='商品图片')
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name
