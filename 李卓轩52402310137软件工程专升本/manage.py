#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import socket

# 修复socket.getfqdn函数以避免Unicode解码错误
original_getfqdn = socket.getfqdn
def fixed_getfqdn(name=''):
    if name:
        try:
            return original_getfqdn(name)
        except UnicodeDecodeError:
            return name
    return 'localhost'
socket.getfqdn = fixed_getfqdn

import os
import sys

# 添加项目根目录和ecommerce目录到sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'ecommerce'))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()