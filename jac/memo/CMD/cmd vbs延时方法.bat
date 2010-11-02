@echo off & setlocal enableextensions enabledelayedexpansion
echo WScript.Sleep 10000 > %temp%\tmp$$$.vbs
echo %time%
cscript //nologo %temp%\tmp$$$.vbs
echo %time%
for %%f in (%temp%\tmp$$$.vbs) do if exist %%f del %%f
endlocal & goto :EOF
