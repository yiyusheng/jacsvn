sc stop WallProxy
sc delete WallProxy
sc create WallProxy binPath= "%~dp0srvany.exe" start= auto
sc description WallProxy "HTTP ������� - WallProxy Ϊ��Ч�͡�"
reg add HKLM\SYSTEM\CurrentControlSet\Services\WallProxy\Parameters /v Application /d "%~dp0..\proxy.exe" /f
reg add HKLM\SYSTEM\CurrentControlSet\Services\WallProxy\Parameters /v AppDirectory /d "%~dp0..\" /f
sc start WallProxy
::@echo.
::@echo ��װ����ɣ�WallProxy �����Ѿ�������
::@echo.
::@echo �����Թر�������ڣ���ʼʹ�ô����ˡ�
::@echo.
::@echo Enjoy it :-)
::@echo.
::@pause