start /min C:\Progra~1\VMware\VMware~1\vmware.exe -x H:\VM\SUSE\SUSE.vmx
ping -n 10 127.0.0.1 >nul 2>nul
taskkill /im vmware.exe /f
exit