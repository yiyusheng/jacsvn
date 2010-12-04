sc stop WallProxy
sc delete WallProxy
sc create WallProxy binPath= "%~dp0srvany.exe" start= auto
sc description WallProxy "HTTP 代理服务 - WallProxy 为您效劳。"
reg add HKLM\SYSTEM\CurrentControlSet\Services\WallProxy\Parameters /v Application /d "%~dp0..\proxy.exe" /f
reg add HKLM\SYSTEM\CurrentControlSet\Services\WallProxy\Parameters /v AppDirectory /d "%~dp0..\" /f
sc start WallProxy
::@echo.
::@echo 安装已完成，WallProxy 服务已经启动。
::@echo.
::@echo 您可以关闭这个窗口，开始使用代理了。
::@echo.
::@echo Enjoy it :-)
::@echo.
::@pause