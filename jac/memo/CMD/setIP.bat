@echo off 
@echo 正在设置IP 
set eth=本地连接 
set ip=110
goto n1 
:n1 
netsh interface ip set address name=%eth% source=static addr=192.168.1.%ip% mask=255.255.255.0 gateway=192.168.1.102 gwmetric=0 >nul 
if not errorlevel 0 set /a ip-=1 & goto n1 
netsh interface ip set dns name=%eth% source=static addr=202.114.0.242 register=PRIMARY >nul 
netsh interface ip add dns name=%eth% addr=202.112.20.131 index=2 >nul 
exit 