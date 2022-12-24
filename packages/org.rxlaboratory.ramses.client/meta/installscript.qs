var targetDirectoryPage = null;
var maintenanceToolName = "";

function Component()
{
    if (installer.isInstaller())
        component.loaded.connect(this, this.addTargetDirWidget);
    maintenanceToolName = installer.value("MaintenanceToolName") + ".exe";
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

    if (systemInfo.productType !== "windows") {
        targetDirectoryPage.RegisterFileCheckBox.hide();
        targetDirectoryPage.AddStartMenuShortcutCheckBox.hide();
        targetDirectoryPage.AddDesktopShortcutCheckBox.hide();
    }
}

Component.prototype.targetChooserClicked = function()
{
    var dir = QFileDialog.getExistingDirectory("", targetDirectoryPage.targetDirectory.text);
    targetDirectoryPage.targetDirectory.setText(dir);
}

Component.prototype.targetDirectoryChanged = function()
{
    var dir = targetDirectoryPage.targetDirectory.text;
    if (installer.fileExists(dir) && installer.fileExists(dir + "/" + maintenanceToolName)) {
        targetDirectoryPage.warning.setText("<p style=\"color: #a526c4\">" + installer.value("Name") + " is already installed. Click the <i>Next</i> button to launch the maintenance tool to update or uninstall it.</p>");

        //installer.finishButtonClicked.connect(this, this.runMaintenanceTool);
        gui.pageById(QInstaller.InstallationFinished).entered.connect(this, this.runMaintenanceTool);

        installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, false);
        installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
        installer.setDefaultPageVisible(QInstaller.PerformInstallation, false);
        installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);

        installer.setValue("RunProgram", "");
        installer.setValue("FinishedText", installer.value("Name") + " is already installed.");

        targetDirectoryPage.RegisterFileCheckBox.hide();
        targetDirectoryPage.AddStartMenuShortcutCheckBox.hide();
        targetDirectoryPage.AddDesktopShortcutCheckBox.hide();

        installer.setValue("TargetDir", dir);
        return;
    }

    installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, true);
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, true);
    installer.setDefaultPageVisible(QInstaller.PerformInstallation, true);
    installer.setDefaultPageVisible(QInstaller.LicenseCheck, true);

    targetDirectoryPage.RegisterFileCheckBox.show();
    targetDirectoryPage.AddStartMenuShortcutCheckBox.show();
    targetDirectoryPage.AddDesktopShortcutCheckBox.show();

    if (installer.fileExists(dir)) {
        targetDirectoryPage.warning.setText("<p style=\"color: red\">Warning: Installing in an existing directory. It will be wiped on uninstallation.</p>");
    }
    else {
        targetDirectoryPage.warning.setText("");
    }
    installer.setValue("TargetDir", dir);
}

Component.prototype.runMaintenanceTool = function()
{
    var dir = installer.value("TargetDir");
    if (installer.fileExists(dir) && installer.fileExists(dir + "/" + maintenanceToolName)) {
        installer.execute(dir + "/" + maintenanceToolName, ["--start-uninstaller"] /*["purge", "-c"]*/);
    }
    else {
        QMessageBox.warning("maintenanceToolNotFound", "Maintenance Tool", "The Maintenance Tool can't be found.");
    }
    gui.clickButton(buttons.FinishButton, 100);
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation
    component.createOperations();

    if (installer.isInstaller() && systemInfo.productType === "windows") {
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
                               "ProgId=org.rxlaboratory.ramses.client");
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
            component.addOperation("CreateShortcut",
                                    "@TargetDir@\\" + maintenanceToolName,
                                    "@StartMenuDir@/Ramses Maintenance Tool.lnk",
                                    "--start-package-manager",
                                    "workingDirectory=@TargetDir@",
                                    "iconPath=@TargetDir@/Ramses_MaintenanceTool.exe",
                                    "iconId=0",
                                    "description=Update or Uninstall Ramses");
        }
    }
}
