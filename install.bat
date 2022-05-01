@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
title Installing FileManager(FM) v1.1.2...
echo Installing FileManager(FM) v1.1.2...
taskkill /f /pid monitor.exe
taskkill /f /pid fm.exe
find "assddff" ..\README.txt
@REM echo %errorlevel%
if "%errorlevel%"=="0" (goto f) else (goto e)
:e
addhkey
set inputname=StartMonitor.lnk
set inputpath=%USERPROFILE%\AppData\Local\Programs\FileManager\fm\
set inputexec=%USERPROFILE%\AppData\Local\Programs\FileManager\fm\restartmonitor.bat
set inputtarget=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp

mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(""%inputtarget%"" & ""\%inputname%""):b.TargetPath=""%inputexec%"":b.WorkingDirectory=""%inputpath%"":b.Save:close")
xcopy /f /h /s release\monitor %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
xcopy /f /h /s release\fm %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
echo Install finished.
pause
start https://yubac.github.io/fmhelp/index.html
exit

:f
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
xcopy /f /h /s release\monitor %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
xcopy /f /h /s release\fm %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
cd ..
cd ..
echo Update finished.
pause
echo Cleaning up residual garbage
rmdir /S /Q fmupdate
exit