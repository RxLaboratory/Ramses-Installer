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

    
}

function _a(text)
{
    QMessageBox.information(
        "debugAlert",
        "Installer Debug Alert",
        text.toString()
    );
}
