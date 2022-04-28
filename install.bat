@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
echo Installing FileManager(FM) v1.0.0...
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
@REM 为monitor添加开机自启动
mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(""%inputtarget%"" & ""\%inputname%""):b.TargetPath=""%inputexec%"":b.WorkingDirectory=""%inputpath%"":b.Save:close")
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
xcopy /f /h /s release\monitor %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
xcopy /f /h /s release\fm %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
echo Install finished.
pause
exit

:f
@REM xcopy /f /h /s %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\id.txt id.txt
@REM xcopy /f /h /s %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\path.txt path.txt
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
xcopy /f /h /s release\monitor %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
xcopy /f /h /s release\fm %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
@REM del /s /q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\id.txt
@REM del /s /q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\path.txt
@REM xcopy /f /h /s id.txt %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\id.txt
@REM xcopy /f /h /s path.txt %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\path.txt
cd ..
cd ..
echo Update finished.
pause
echo Cleaning up residual garbage
rmdir /S /Q fmupdate
exit