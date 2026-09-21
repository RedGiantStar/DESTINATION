@echo off

REM 切换到前端目录
cd /d "E:\李卓轩52402310137软件工程专升本\frontend"

echo 当前目录: %cd%
echo.

REM 设置Node.js路径
set "NODE_HOME=D:\Program Files\node-v24.13.1-win-x64"
set "PATH=%NODE_HOME%;%NODE_HOME%\node_modules\npm\bin;%PATH%"

echo Node.js路径: %NODE_HOME%
echo.

REM 检查npm是否可用
echo 检查npm版本...
npm --version
echo.

REM 安装依赖
echo 安装前端依赖...
npm install
echo.

REM 启动开发服务器
echo 启动前端开发服务器...
npm run dev

pause
