function Component()
{
    
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation
    component.createOperations();

    // Windows
    if (systemInfo.productType === "windows") {
        if (installer.isInstaller() || installer.isUpdater()) {

            var ramsesPath = "@TargetDir@\\client\\ramses.exe";
            var maintenancePath = "@TargetDir@\\" + installer.value("MaintenanceToolName") + ".exe";

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
