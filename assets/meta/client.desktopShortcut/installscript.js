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
                   
            console.log("Creating desktop shortcut.");
            component.addOperation("CreateShortcut",
                                    ramsesPath,
                                    "@DesktopDir@/Ramses.lnk",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=" + ramsesPath,
                                    "iconId=0",
                                    "description=Run Ramses");
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
