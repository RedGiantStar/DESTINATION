@echo off

REM 前端启动脚本

echo 启动前端开发服务器...
echo.

REM 设置Node.js路径
set NODE_HOME=D:\Program Files\node-v24.13.1-win-x64
set PATH=%NODE_HOME%;%NODE_HOME%\node_modules\npm\bin;%PATH%

REM 检查npm版本
echo 检查npm版本...
npm --version
echo.

REM 启动开发服务器
echo 启动Vite开发服务器...
npm run dev

pause
