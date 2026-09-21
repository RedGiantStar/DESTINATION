#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = '创建默认管理员账号'

    def handle(self, *args, **options):
        # 检查是否已存在admin用户
        if User.objects.filter(username='admin').exists():
            self.stdout.write(
                self.style.WARNING('管理员账号 admin 已存在')
            )
            # 更新密码
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(
                self.style.SUCCESS('管理员密码已更新为: admin123')
            )
        else:
            # 创建新的管理员
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                phone='13800138000',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('管理员账号创建成功!')
            )
            self.stdout.write('用户名: admin')
            self.stdout.write('密码: admin123')
            self.stdout.write('登录地址: http://localhost:8000/admin/')
