var isWin = systemInfo.kernelType == "winnt";
var isMac = systemInfo.kernelType == "darwin";
var isLinux = systemInfo.kernelType == "linux";

function Component()
{
    installer.installationFinished.connect(this, Component.prototype.installationFinishedPageIsShown);
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation
    component.createOperations();

    // Windows
    if (isWin) {
        if (installer.isInstaller()) {
            var registerFile = installer.value("registerFileType", true);
    
            var iconId = 0;
            var ramsesPath = "@TargetDir@\\client\\ramses.exe";
    
            if (registerFile) {
                console.log("Registering *.ramses files.");
                component.addOperation("RegisterFileType",
                                   "ramses",
                                   ramsesPath + " '%1'",
                                   "Ramses Database",
                                   "application/x-sqlite3",
                                   ramsesPath + "," + iconId,
                                   "ProgId=org.rxlaboratory.ramses.client");
            }

        }
    }
    else if (isLinux) {

        var maintenancePath = "@TargetDir@/" + installer.value("MaintenanceToolName");
        
        component.addOperation("InstallIcons",
            "@TargetDir@/client/share/icons"
        );

        component.addOperation("CreateDesktopEntry",
            "@HomeDir@/.local/share/applications/Ramses.desktop",
            "Type=Application\n" +
            "Name=Ramses\n" +
            "GenericName=Asset and Production Manager\n" +
            "Comment=The Rx Asset Management System, asset management and production tracking.\n" +
            "Exec=@TargetDir@/client/bin/ramses\n" +
            "Icon=ramses\n" +
            "Categories=AudioVideo;ProjectManagement;Qt"
        );

        component.addOperation("CreateDesktopEntry",
            "@HomeDir@/.local/share/applications/Ramses Maintenance Tool.desktop",
            "Type=Application\n" +
            "Name=Ramses Maintenance Tool\n" +
            "GenericName=Maintenance tool\n" +
            "Comment=Add, Update or Remove Ramses components.\n" +
            "Exec=" + maintenancePath + "\n" +
            "Icon=ramses-maintenancetool\n" +
            "Categories=AudioVideo;ProjectManagement;Qt"
        );
    }
}

Component.prototype.installationFinishedPageIsShown = function()
{
    if (isMac && installer.isInstaller() && installer.status == QInstaller.Success) {
        // Set the dir icon
        installer.executeDetached(
            "bash",
            ["-c", "@TargetDir@/set_folder_icon.sh"],
            installer.value("TargetDir")
        )
        // Set the maintenance tool icon
        installer.performOperation(
            "Move",
            [
                "@TargetDir@/ramses-maintenancetool.icns",
                "@TargetDir@/Ramses Maintenance Tool.app/Contents/Resources/ramses-maintenancetool.icns"
            ]
        );
        installer.performOperation(
            "Replace",
            [
                "@TargetDir@/Ramses Maintenance Tool.app/Contents/Info.plist",
                "</dict>",
                "\t<key>CFBundleIconFile</key>\n\t<string>ramses-maintenancetool.icns</string>\n</dict>",
                "string"
            ]
        );
    }
}

function _a(text)
{
    QMessageBox.information(
        "debugAlert",
        "Installer Debug Alert",
        text.toString()
    );
}
