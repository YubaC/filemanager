@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
title Installing FileManager(FM) v1.1.9...
echo Installing FileManager(FM) v1.1.9...
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
xcopy /f /h /s release\lib %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
echo Install finished.
pause
start https://yubac.github.io/fmhelp/index.html
start https://yubac.github.io/fmhelp/whats_new_in_this_release.html
exit

:f
copy %USERPROFILE%\AppData\Local\Programs\FileManager\fm\path.txt .\
copy %USERPROFILE%\AppData\Local\Programs\FileManager\fm\id.txt .\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
rmdir /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\lib\
xcopy /f /h /s release\monitor %USERPROFILE%\AppData\Local\Programs\FileManager\monitor\
xcopy /f /h /s release\fm %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
xcopy /f /h /s release\lib %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
del /F /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\path.txt
del /F /S /Q %USERPROFILE%\AppData\Local\Programs\FileManager\fm\id.txt
copy .\path.txt %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
copy .\id.txt %USERPROFILE%\AppData\Local\Programs\FileManager\fm\
cd ..
cd ..
echo Update finished.
pause
echo Cleaning up residual garbage
start https://yubac.github.io/fmhelp/whats_new_in_this_release.html
rmdir /S /Q fmupdate
exit