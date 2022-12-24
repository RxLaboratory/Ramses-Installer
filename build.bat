rd /s /q "repository"
C:\Qt\Tools\QtInstallerFramework\4.5\bin\repogen.exe -p packages repository

echo " " > "repository\style.css"
echo " " > "repository\index.html"
xcopy /Y html\style.css "repository\style.css"
xcopy /Y html\index.html "repository\index.html"

C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages build/Ramses_Offline-Installer.exe
C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages -n build/Ramses_Online-Installer.exe

REM C:\Qt\Tools\QtInstallerFramework\4.5\bin\binarycreator.exe -c config/config.xml -p packages -rcc