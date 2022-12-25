var targetDirectoryPage = null;
var maintenanceToolName = "";
var doRunMaintenanceTool = false;

function Component()
{
    setupUi();    
    maintenanceToolName = installer.value("MaintenanceToolName") + ".exe";
}

// Here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{   

    // call default implementation
    component.createOperations();

    if (installer.isInstaller() && systemInfo.productType === "windows") {
        var registerFile = targetDirectoryPage.RegisterFileCheckBox.checked;
        var createDesktopShortcut = targetDirectoryPage.AddDesktopShortcutCheckBox.checked;
        var createStartMenuShortcut = targetDirectoryPage.addStartMenuShortcutBox.checked;

        var iconId = 0;
        var ramsesPath = "@TargetDir@\\ramses.exe";
        var maintenancePath = "@TargetDir@\\" + maintenanceToolName;

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

function setupUi()
{
    if (installer.isInstaller()) {
        // Hide components selection if only a single one (+ the maintenance tool)
        if (installer.components().length <= 2) installer.setDefaultPageVisible(QInstaller.ComponentSelection, false);
        // Setup our own target widget
        component.loaded.connect(this, addTargetDirWidget);
        gui.pageById(QInstaller.InstallationFinished).entered.connect(this, runMaintenanceTool);
    }
    if (!installer.isUninstaller()) {
        component.loaded.connect(this, addFinishWidget);
        installer.finishButtonClicked.connect(this, contribute);
    }
}

function showStartMenuPage()
{
    var show = targetDirectoryPage.addStartMenuShortcutBox.checked;
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, show);
}

function addTargetDirWidget()
{
    // Hide the target dir to add our own
    installer.setDefaultPageVisible(QInstaller.TargetDirectory, false);
    installer.addWizardPage(component, "TargetWidget", QInstaller.TargetDirectory);

    // Setup UI
    targetDirectoryPage = gui.pageWidgetByObjectName("DynamicTargetWidget");
    targetDirectoryPage.windowTitle = "Choose Installation Directory";
    targetDirectoryPage.description.setText("Please select where " + installer.value("Name") + " will be installed:");
    targetDirectoryPage.targetDirectory.textChanged.connect(this, changeTargetDir);
    targetDirectoryPage.targetDirectory.setText(installer.value("TargetDir"));
    targetDirectoryPage.targetChooser.released.connect(this, chooseTargetDialog);
    targetDirectoryPage.addStartMenuShortcutBox.clicked.connect(this, showStartMenuPage);

    if (systemInfo.productType !== "windows") {
        targetDirectoryPage.RegisterFileCheckBox.hide();
        targetDirectoryPage.addStartMenuShortcutBox.hide();
        targetDirectoryPage.AddDesktopShortcutCheckBox.hide();
    }
}

function addFinishWidget()
{
    installer.addWizardPageItem(component, "FinishWidget", QInstaller.InstallationFinished);
}

function chooseTargetDialog()
{
    var dir = QFileDialog.getExistingDirectory("Select a directory to install " + installer.value("Name"), targetDirectoryPage.targetDirectory.text);
    dir = installer.toNativeSeparators(dir);
    targetDirectoryPage.targetDirectory.setText(dir);
}

function changeTargetDir()
{
    var dir = targetDirectoryPage.targetDirectory.text;
    installer.setValue("TargetDir", dir);

    if (installer.fileExists(dir) && installer.fileExists(dir + "/" + maintenanceToolName)) {
        targetDirectoryPage.warning.setText("<p style=\"color: #a526c4\">" + installer.value("Name") + " is already installed. Click the <i>Next</i> button to launch the maintenance tool to update or uninstall it.</p>");

        doRunMaintenanceTool = true;

        installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, false);
        installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
        installer.setDefaultPageVisible(QInstaller.PerformInstallation, false);
        installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);

        targetDirectoryPage.RegisterFileCheckBox.hide();
        targetDirectoryPage.addStartMenuShortcutBox.hide();
        targetDirectoryPage.AddDesktopShortcutCheckBox.hide();

        return;
    }

    installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, true);
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, true);
    installer.setDefaultPageVisible(QInstaller.PerformInstallation, true);
    installer.setDefaultPageVisible(QInstaller.LicenseCheck, true);

    targetDirectoryPage.RegisterFileCheckBox.show();
    targetDirectoryPage.addStartMenuShortcutBox.show();
    targetDirectoryPage.AddDesktopShortcutCheckBox.show();

    if (installer.fileExists(dir)) {
        var files = QDesktopServices.findFiles(dir, "*");
        if (files.length > 0) {
            targetDirectoryPage.warning.setText("<p style=\"color: red\">Warning: Installing in an existing directory. It will be wiped on uninstallation.</p>");
            return;
        }
    }
    
    targetDirectoryPage.warning.setText("");
}

function runMaintenanceTool()
{
    if (!doRunMaintenanceTool) return;

    var dir = installer.value("TargetDir");
    if (installer.fileExists(dir) && installer.fileExists(dir + "/" + maintenanceToolName)) {
        installer.executeDetached(dir + "/" + maintenanceToolName, ["--start-uninstaller"] /*["purge", "-c"]*/);
    }
    else {
        QMessageBox.warning("maintenanceToolNotFound", "Maintenance Tool", "The Maintenance Tool can't be found.");
    }
    gui.rejectWithoutPrompt();
}

function contribute()
{
    var widget = component.userInterface( "FinishWidget" );

    if (gui.findChild(widget, "membershipButton").checked) {
        QDesktopServices.openUrl("http://membership.rxlab.info");
    }
    else if (gui.findChild(widget, "commercialButton").checked) {
        QDesktopServices.openUrl("https://rxlaboratory.org/product/rx-open-tools-professional-contribution/");
    }
    else if (gui.findChild(widget, "nonProfitButton").checked) {
        QDesktopServices.openUrl("https://rxlaboratory.org/product/one-time-donation/");
    }
    else if (gui.findChild(widget, "giveAHandButton").checked) {
        QDesktopServices.openUrl("http://contribute.rxlab.info/");
    }
}