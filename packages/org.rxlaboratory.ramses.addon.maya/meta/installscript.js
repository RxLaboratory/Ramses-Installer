function Component()
{

}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   
    // call default implementation
    component.createOperations();

    // Copy mod to documents/maya/modules
    var modPath = "@TargetDir@/maya/";
    var modFile = modPath + "Ramses.mod";

    component.addOperation("Replace",
                            modFile,
                            "D:\\Path\\To\\Ramses-Maya",
                            modPath
                            );

    // Create dir
    var destPath = QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation) + "/maya";
    if (!installer.fileExists(destPath))
        component.addOperation("Mkdir",
                            destPath
                            );

    destPath += "/modules"
    if (!installer.fileExists(destPath))
        component.addOperation("Mkdir",
                            destPath
                            );

    component.addOperation("Copy",
                            modFile,
                            destPath + "/Ramses.mod"
                            );
}

function _a(text)
{
    QMessageBox.information(
        "debugAlert",
        "Installer Debug Alert",
        text.toString()
    );
}
