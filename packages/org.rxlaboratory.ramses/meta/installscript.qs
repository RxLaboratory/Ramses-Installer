var targetDirectoryPage = null;

function Component()
{
    component.loaded.connect(this, this.addTargetDirWidget);
}

Component.prototype.addTargetDirWidget = function()
{
    // Hide the target dir to add our own
    installer.setDefaultPageVisible(QInstaller.TargetDirectory, false);
    installer.addWizardPage(component, "TargetWidget", QInstaller.TargetDirectory);

    // Setup UI
    targetDirectoryPage = gui.pageWidgetByObjectName("DynamicTargetWidget");
    targetDirectoryPage.windowTitle = "Choose Installation Directory";
    targetDirectoryPage.description.setText("Please select where " + installer.value("Name") + " will be installed:");
    targetDirectoryPage.targetDirectory.textChanged.connect(this, this.targetDirectoryChanged);
    targetDirectoryPage.targetDirectory.setText(installer.value("TargetDir"));
    targetDirectoryPage.targetChooser.released.connect(this, this.targetChooserClicked);

    if (!installer.isInstaller() || systemInfo.productType !== "windows") {
        targetDirectoryPage.RegisterFileCheckBox.hide();
    }

    if (systemInfo.productType !== "windows") {
        targetDirectoryPage.AddStartMenuShortcutCheckBox.hide();
        targetDirectoryPage.AddDesktopShortcutCheckBox.hide();
    }

    gui.pageById(QInstaller.LicenseCheck).entered.connect(this, this.licensePageEntered);
}

Component.prototype.targetChooserClicked = function()
{
    var dir = QFileDialog.getExistingDirectory("", targetDirectoryPage.targetDirectory.text);
    targetDirectoryPage.targetDirectory.setText(dir);
}

Component.prototype.targetDirectoryChanged = function()
{
    var dir = targetDirectoryPage.targetDirectory.text;
    if (installer.fileExists(dir) && installer.fileExists(dir + "/maintenancetool.exe")) {
        targetDirectoryPage.warning.setText("<p style=\"color: #a526c4\">" + installer.value("Name") + " is already installed. It will be uninstalled when going to the next page.</p>");
    }
    else if (installer.fileExists(dir)) {
        targetDirectoryPage.warning.setText("<p style=\"color: red\">Warning: Installing in an existing directory. It will be wiped on uninstallation.</p>");
    }
    else {
        targetDirectoryPage.warning.setText("");
    }
    installer.setValue("TargetDir", dir);
}

Component.prototype.licensePageEntered = function()
{
    var dir = installer.value("TargetDir");
    if (installer.fileExists(dir) && installer.fileExists(dir + "/maintenancetool.exe")) {
        installer.gainAdminRights();
        installer.execute(dir + "/maintenancetool.exe", ["purge", "-c"]);
    }
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation to actually install the registeredfile
    component.createOperations();

    if (systemInfo.productType === "windows") {
        targetDirectoryPage = gui.pageWidgetByObjectName("DynamicTargetWidget");
        var registerFile = targetDirectoryPage.RegisterFileCheckBox.checked;
        var createDesktopShortcut = targetDirectoryPage.AddDesktopShortcutCheckBox.checked;
        var createStartMenuShortcut = targetDirectoryPage.AddStartMenuShortcutCheckBox.checked;

        var iconId = 0;
        var ramsesPath = installer.value("TargetDir") + "\\ramses.exe";

        if (registerFile) {
            console.log("Registering *ramses files.");
            component.addOperation("RegisterFileType",
                               "ramses",
                               ramsesPath + " '%1'",
                               "Ramses Database",
                               "application/x-sqlite3",
                               ramsesPath + "," + iconId,
                               "ProgId=org.rxlaboratory.ramses");
        }

        if (createDesktopShortcut) {
            console.log("Creating desktop shortcut.");
            component.addOperation("CreateShortcut",
                                    ramsesPath,
                                    "@DesktopDir@/Ramses.lnk",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=@TargetDir@/ramses.exe",
                                    "iconId=0",
                                    "description=Run Ramses");
        }

        if (createStartMenuShortcut) {
            console.log("Creating start menu shortcut.");
            component.addOperation("CreateShortcut",
                                    ramsesPath,
                                    "@StartMenuDir@/Ramses.lnk",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=@TargetDir@/ramses.exe",
                                    "iconId=0",
                                    "description=Run Ramses");
        }
       
    }
}
