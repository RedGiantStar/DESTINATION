# PowerShell脚本 - 创建管理员账号
Write-Host "================================================" -ForegroundColor Green
Write-Host "       正在创建管理员账号..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# 切换到脚本所在目录
Set-Location -Path $PSScriptRoot

# 执行Python命令创建管理员
python manage.py shell -c @"
from accounts.models import User
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@example.com', 'admin123', phone='13800138000')
print('管理员创建成功!')
print('用户名: admin')
print('密码: admin123')
print('请登录 http://localhost:8000/admin/')
"@

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "       管理员账号创建完成！" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "请使用以下信息登录管理后台:" -ForegroundColor Cyan
Write-Host "  用户名: admin" -ForegroundColor Yellow
Write-Host "  密码: admin123" -ForegroundColor Yellow
Write-Host "  地址: http://localhost:8000/admin/" -ForegroundColor Cyan
Write-Host ""
pause
