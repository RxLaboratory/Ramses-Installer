REM rd /s /q "repository"
REM C:\Qt\Tools\QtInstallerFramework\4.5\bin\repogen.exe -p packages repository
C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages build/Ramses_Offline-Installer.exe
REM C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages -n build/Ramses_Online-Installer.exe