import subprocess
import sys

print("=" * 50)
print("       E-commerce System Launcher")
print("=" * 50)
print()

print("[Start] Django Backend Server...")
backend = subprocess.Popen([
    'powershell', '-Command',
    'Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d E:\\李卓轩52402310137软件工程专升本 && python manage.py runserver 127.0.0.1:8000" -WindowStyle Normal'
])

import time
time.sleep(3)

print("[Start] Vue Frontend Server...")
frontend = subprocess.Popen([
    'powershell', '-Command',
    'Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d E:\\李卓轩52402310137软件工程专升本\\frontend && `\"D:\\Program Files\\node-v24.13.1-win-x64\\node.exe`\" node_modules/vite/bin/vite.js --host 0.0.0.0 --port 5173" -WindowStyle Normal'
])

print("\n" + "=" * 50)
print("Startup Complete!")
print("=" * 50)
print()
print("Frontend: http://localhost:5173")
print("Backend:  http://localhost:8000")
print()
print("Press Enter to stop all services...")
input()

print("\nStopping services...")
subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], capture_output=True)
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
print("All services stopped.")