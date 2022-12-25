function Component()
{
    
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation
    component.createOperations();

    if (installer.isInstaller() && systemInfo.productType === "windows") {
        var registerFile = installer.value("registerFileType", true);
        var createDesktopShortcut = installer.value("addDesktopShortcut", false);
        var createStartMenuShortcut = installer.value("addStartMenuShortcut", true);

        var iconId = 0;
        var ramsesPath = "@TargetDir@\\client\\ramses.exe";
        var maintenancePath = "@TargetDir@\\" + installer.value("MaintenanceToolName") + ".exe";;

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

        if (createDesktopShortcut) {
            console.log("Creating desktop shortcut.");
            component.addOperation("CreateShortcut",
                                    ramsesPath,
                                    "@DesktopDir@/Ramses.lnk",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=" + ramsesPath,
                                    "iconId=0",
                                    "description=Run Ramses");
        }

        if (createStartMenuShortcut) {
            console.log("Creating start menu shortcut.");
            component.addOperation("CreateShortcut",
                                    ramsesPath,
                                    "@StartMenuDir@/Ramses.lnk",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=" + ramsesPath,
                                    "iconId=0",
                                    "description=Run Ramses");
            component.addOperation("CreateShortcut",
                                    maintenancePath,
                                    "@StartMenuDir@/Ramses Maintenance Tool.lnk",
                                    "--start-package-manager",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=" + maintenancePath,
                                    "iconId=0",
                                    "description=Update or Uninstall Ramses");
        }
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
