#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = '添加演示数据'

    def handle(self, *args, **options):
        self.stdout.write('开始添加演示数据...\n')
        
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('已删除现有数据\n')
        
        self.stdout.write('创建商品分类...')
        
        categories = {
            '数码': ['手机', '电脑', '平板', '智能手表', '耳机'],
            '家电': ['电视', '空调', '冰箱', '洗衣机', '厨房电器'],
            '服饰': ['男装', '女装', '鞋靴', '箱包'],
            '美妆': ['护肤', '彩妆', '香水', '个人护理'],
            '食品': ['零食', '生鲜', '调料', '饮料'],
            '图书': ['小说', '教育', '科技', '经济']
        }
        
        category_objects = {}
        
        for parent_name, sub_categories in categories.items():
            parent_category, _ = Category.objects.get_or_create(
                name=parent_name,
                defaults={'is_active': True}
            )
            category_objects[parent_name] = parent_category
            self.stdout.write(f'  创建一级分类: {parent_name}')
            
            for sub_name in sub_categories:
                sub_category, _ = Category.objects.get_or_create(
                    name=sub_name,
                    parent=parent_category,
                    defaults={'is_active': True}
                )
                category_objects[sub_name] = sub_category
                self.stdout.write(f'    创建二级分类: {sub_name}')
        
        self.stdout.write('分类创建完成\n')
        
        self.stdout.write('创建演示商品...')
        
        demo_products = [
            {
                'name': 'iPhone 15 Pro Max 256GB',
                'category': '手机',
                'price': 9999.00,
                'stock': 50,
                'description': '全新旗舰，支持全网通，搭载A17 Pro芯片'
            },
            {
                'name': 'MacBook Pro 14英寸 M3 Pro',
                'category': '电脑',
                'price': 14999.00,
                'stock': 30,
                'description': 'M3 Pro芯片，18GB统一内存'
            },
            {
                'name': 'iPad Pro 12.9英寸 M2',
                'category': '平板',
                'price': 8999.00,
                'stock': 40,
                'description': 'M2芯片，Liquid Retina XDR显示屏'
            },
            {
                'name': 'Apple Watch Series 9',
                'category': '智能手表',
                'price': 2999.00,
                'stock': 60,
                'description': 'S9 SiP芯片，全天候显示屏'
            },
            {
                'name': 'AirPods Pro 2代',
                'category': '耳机',
                'price': 1899.00,
                'stock': 80,
                'description': '主动降噪，自适应通透模式'
            },
            {
                'name': '小米电视6 65英寸 OLED',
                'category': '电视',
                'price': 5999.00,
                'stock': 25,
                'description': '4K OLED自发光屏幕'
            },
            {
                'name': '格力空调 1.5匹',
                'category': '空调',
                'price': 3299.00,
                'stock': 35,
                'description': '新一级能效，变频节能'
            },
            {
                'name': '西门子冰箱 549升',
                'category': '冰箱',
                'price': 4999.00,
                'stock': 20,
                'description': '549升大容量，风冷无霜'
            },
            {
                'name': '优衣库羽绒服',
                'category': '男装',
                'price': 599.00,
                'stock': 100,
                'description': '90%鸭绒，轻薄保暖'
            },
            {
                'name': 'ZARA连衣裙',
                'category': '女装',
                'price': 399.00,
                'stock': 80,
                'description': '时尚设计，优质面料'
            },
            {
                'name': '兰蔻小黑瓶精华液 50ml',
                'category': '护肤',
                'price': 1080.00,
                'stock': 50,
                'description': '基底修护，焕亮肤色'
            },
            {
                'name': 'YSL小金条口红',
                'category': '彩妆',
                'price': 380.00,
                'stock': 120,
                'description': '哑光质地，显色持久'
            },
            {
                'name': '三只松鼠坚果礼盒',
                'category': '零食',
                'price': 128.00,
                'stock': 200,
                'description': '多种坚果组合，新鲜美味'
            },
            {
                'name': '农夫山泉天然水 24瓶',
                'category': '饮料',
                'price': 36.00,
                'stock': 500,
                'description': '天然矿泉水，口感清甜'
            },
            {
                'name': '三体全集',
                'category': '小说',
                'price': 98.00,
                'stock': 150,
                'description': '刘慈欣代表作'
            },
            {
                'name': 'Python编程从入门到实践',
                'category': '科技',
                'price': 89.00,
                'stock': 100,
                'description': 'Python入门经典'
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
                self.stdout.write(f'  创建商品: {product_data["name"]}')
        
        self.stdout.write('商品创建完成\n')
        
        category_count = Category.objects.filter(is_active=True).count()
        product_count = Product.objects.filter(is_active=True).count()
        
        self.stdout.write(f'\n演示数据添加完成!')
        self.stdout.write(f'统计信息:')
        self.stdout.write(f'   - 商品分类: {category_count} 个')
        self.stdout.write(f'   - 演示商品: {product_count} 个')
