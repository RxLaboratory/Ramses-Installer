@echo off

:: Generate .rcc file
cd packages
cd org.rxlaboratory.ifw.maintenancetool
cd data
C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c ../../../config/config.xml -p ../../../packages -rcc
cd ..
cd ..
cd ..

:: Generate the new repo (update mode)
rd /s /q "repository"
C:\Qt\Tools\QtInstallerFramework\4.5\bin\repogen.exe --update -p packages repository/win

:: Generate installer binaries
del "build\Ramses_Offline-Installer.exe"
del "build\Ramses_Online-Installer.exe"
C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages build/Ramses_Offline-Installer.exe
C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages -n build/Ramses_Online-Installer.exe

exit /b 

:FindReplace <findstr> <replstr> <file>
set tmp="%temp%\tmp.txt"
If not exist %temp%\_.vbs call :MakeReplace
for /f "tokens=*" %%a in ('dir "%3" /s /b /a-d /on') do (
  for /f "usebackq" %%b in (`Findstr /mic:"%~1" "%%a"`) do (
    echo(&Echo Replacing "%~1" with "%~2" in file %%~nxa
    <%%a cscript //nologo %temp%\_.vbs "%~1" "%~2">%tmp%
    if exist %tmp% move /Y %tmp% "%%~dpnxa">nul
  )
)
del %temp%\_.vbs
exit /b

:MakeReplace
>%temp%\_.vbs echo with Wscript
>>%temp%\_.vbs echo set args=.arguments
>>%temp%\_.vbs echo .StdOut.Write _
>>%temp%\_.vbs echo Replace(.StdIn.ReadAll,args(0),args(1),1,-1,1)
>>%temp%\_.vbs echo end with