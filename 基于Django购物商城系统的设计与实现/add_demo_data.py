#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import socket

# 保存原始的getfqdn函数
original_getfqdn = socket.getfqdn

# 重写getfqdn函数来绕过主机名解析问题
def custom_getfqdn(name=''):
    if name:
        try:
            return original_getfqdn(name)
        except UnicodeDecodeError:
            return name
    return 'localhost'

# 替换原始函数
socket.getfqdn = custom_getfqdn

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

# 添加项目根目录和ecommerce目录到Python路径
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'ecommerce'))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# 导入Django
import django
django.setup()

from products.models import Category, Product

print('开始添加演示数据...\n')

# 清除现有数据
print('清除现有数据...')
Product.objects.all().delete()
Category.objects.all().delete()
print('清除完成\n')

# 创建分类（参考京东/淘宝分类）
print('创建商品分类...')

# 一级分类
categories = {
    '数码': ['手机', '电脑', '平板', '智能手表', '耳机'],
    '家电': ['电视', '空调', '冰箱', '洗衣机', '厨房电器'],
    '服饰': ['男装', '女装', '童装', '鞋靴', '箱包'],
    '美妆': ['护肤', '彩妆', '香水', '个护', '美发'],
    '食品': ['零食', '生鲜', '饮料', '粮油', '酒水'],
    '图书': ['小说', '教育', '科技', '经管', '文学']
}

category_objects = {}

for parent_name, sub_categories in categories.items():
    parent_category, _ = Category.objects.get_or_create(
        name=parent_name,
        defaults={'is_active': True}
    )
    category_objects[parent_name] = parent_category
    print(f'  创建一级分类: {parent_name}')
    
    for sub_name in sub_categories:
        sub_category, _ = Category.objects.get_or_create(
            name=sub_name,
            parent=parent_category,
            defaults={'is_active': True}
        )
        category_objects[sub_name] = sub_category
        print(f'    创建二级分类: {sub_name}')

print('分类创建完成\n')

# 创建演示商品
print('创建演示商品...')

demo_products = [
    # 数码类
    {
        'name': 'iPhone 15 Pro Max 256GB',
        'category': '手机',
        'price': 9999.00,
        'stock': 50,
        'description': '全新正品，支持全国联保，搭载A17 Pro芯片，钛金属边框，专业级摄像系统'
    },
    {
        'name': 'MacBook Pro 14英寸 M3 Pro',
        'category': '电脑',
        'price': 14999.00,
        'stock': 30,
        'description': 'M3 Pro芯片，18GB统一内存，512GB固态硬盘，Liquid Retina XDR显示屏'
    },
    {
        'name': 'iPad Pro 12.9英寸 M2',
        'category': '平板',
        'price': 8999.00,
        'stock': 40,
        'description': 'M2芯片，12.9英寸Liquid Retina XDR显示屏，支持Apple Pencil和Magic Keyboard'
    },
    {
        'name': 'Apple Watch Series 9',
        'category': '智能手表',
        'price': 2999.00,
        'stock': 60,
        'description': 'S9 SiP芯片，全天候视网膜显示屏，摔倒检测，ECG心电图'
    },
    {
        'name': 'AirPods Pro 2代',
        'category': '耳机',
        'price': 1899.00,
        'stock': 80,
        'description': '主动降噪，自适应通透模式，空间音频，续航时间更长'
    },
    
    # 家电类
    {
        'name': '小米电视6 65英寸 OLED',
        'category': '电视',
        'price': 5999.00,
        'stock': 25,
        'description': '4K OLED自发光屏幕，120Hz高刷新率，MEMC运动补偿，杜比视界'
    },
    {
        'name': '格力空调 1.5匹 新一级能效',
        'category': '空调',
        'price': 3299.00,
        'stock': 35,
        'description': '新一级能效，变频节能，静音设计，智能WiFi控制'
    },
    {
        'name': '海尔冰箱 549升 对开门',
        'category': '冰箱',
        'price': 4999.00,
        'stock': 20,
        'description': '549升大容量，风冷无霜，变频节能，智能控温'
    },
    
    # 服饰类
    {
        'name': '优衣库羽绒服 男士',
        'category': '男装',
        'price': 599.00,
        'stock': 100,
        'description': '90%白鸭绒，轻盈保暖，防风防水，多色可选'
    },
    {
        'name': 'ZARA连衣裙 女士',
        'category': '女装',
        'price': 399.00,
        'stock': 80,
        'description': '时尚设计，优质面料，修身版型，多色可选'
    },
    
    # 美妆类
    {
        'name': '兰蔻小黑瓶精华液 50ml',
        'category': '护肤',
        'price': 1080.00,
        'stock': 50,
        'description': '肌底修护，淡化细纹，提亮肤色，提升肌肤光泽'
    },
    {
        'name': 'YSL小金条口红',
        'category': '彩妆',
        'price': 380.00,
        'stock': 120,
        'description': '丝滑质地，持久显色，滋润不拔干，多色号可选'
    },
    
    # 食品类
    {
        'name': '三只松鼠坚果礼盒',
        'category': '零食',
        'price': 128.00,
        'stock': 200,
        'description': '多种坚果组合，新鲜美味，营养健康，送礼佳品'
    },
    {
        'name': '农夫山泉天然水 24瓶',
        'category': '饮料',
        'price': 36.00,
        'stock': 500,
        'description': '天然矿泉水，弱碱性，甘甜可口，550ml*24瓶'
    },
    
    # 图书类
    {
        'name': '三体全集 刘慈欣',
        'category': '小说',
        'price': 98.00,
        'stock': 150,
        'description': '雨果奖获奖作品，中国科幻里程碑，三体三部曲完整版'
    },
    {
        'name': 'Python编程从入门到实践',
        'category': '科技',
        'price': 89.00,
        'stock': 100,
        'description': 'Python入门经典，从零开始学习编程，项目驱动式教学'
    }
]

for product_data in demo_products:
    category = category_objects.get(product_data['category'])
    if category:
        Product.objects.create(
            name=product_data['name'],
            category=category,
            price=product_data['price'],
            stock=product_data['stock'],
            description=product_data['description'],
            is_active=True
        )
        print(f'  创建商品: {product_data["name"]} - ￥{product_data["price"]}')

print('商品创建完成\n')

# 统计
category_count = Category.objects.filter(is_active=True).count()
product_count = Product.objects.filter(is_active=True).count()

print(f'演示数据添加完成！')
print(f'统计信息:')
print(f'   - 商品分类: {category_count} 个')
print(f'   - 演示商品: {product_count} 个')
print(f'\n访问系统查看效果')
