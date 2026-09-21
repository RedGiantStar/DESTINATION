#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端启动脚本
使用Python来启动前端开发服务器
"""

import os
import subprocess
import time
from pathlib import Path

def main():
    """主函数"""
    print("启动前端开发服务器...\n")
    
    # 设置Node.js路径
    node_home = r'D:\Program Files\node-v24.13.1-win-x64'
    npm_cmd = os.path.join(node_home, 'npm.cmd')
    
    # 检查npm.cmd是否存在
    if not os.path.exists(npm_cmd):
        print(f"npm.cmd不存在: {npm_cmd}")
        return False
    
    print(f"找到npm.cmd: {npm_cmd}")
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查package.json是否存在
    package_json = os.path.join(current_dir, 'package.json')
    if not os.path.exists(package_json):
        print(f"package.json不存在: {package_json}")
        return False
    
    print("package.json存在")
    
    # 启动前端服务器
    print("\n启动Vite开发服务器...")
    print("=====================================")
    
    try:
        # 运行npm run dev命令
        process = subprocess.Popen(
            [npm_cmd, 'run', 'dev'],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 读取输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                # 检查是否启动成功
                if 'Local:' in output:
                    print("\n前端服务器启动成功！")
                    print("=====================================")
                    print("请在浏览器中打开上述地址访问电商系统")
                    print("按 Ctrl+C 停止服务器")
                    print("=====================================")
    
        # 等待进程结束
        process.wait()
        
    except Exception as e:
        print(f"启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
