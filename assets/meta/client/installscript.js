var isWin = systemInfo.kernelType == "winnt";
var isMac = systemInfo.kernelType == "darwin";
var isLinux = systemInfo.kernelType == "linux";
var targetDirectoryPage = null;
var maintenanceToolName = "";
var finishWidget = null;
var doRunMaintenanceTool = false;

function Component()
{
    maintenanceToolName = installer.value("MaintenanceToolName")
    if (isWin) maintenanceToolName += ".exe";
    if (isMac) maintenanceToolName += ".app";

    setupUi();
    setupComponents();
}

function setupUi()
{
    if (installer.isInstaller()) {
        // Hide components selection if only a single one (+ the maintenance tool)
        if (installer.components().length <= 2) installer.setDefaultPageVisible(QInstaller.ComponentSelection, false);
        // Setup our own target widget
        //component.loaded.connect(this, addTargetDirWidget);
        addTargetDirWidget();
        gui.pageById(QInstaller.ComponentSelection).entered.connect(this, runMaintenanceTool);
        gui.pageById(QInstaller.ReadyForInstallation).entered.connect(this, prepareInstallation);
        gui.pageById(QInstaller.LicenseCheck).entered.connect(this, showHideStartMenuPage);
    }
}

function setupComponents()
{
    var components = installer.components( ".+\\.desktopShortcut$" );
    components = components.concat( installer.components( ".+\\.startMenuShortcut$" ) );
    for (var i = 0; i < components.length; i++) {
        components[i].enabled = isWin;
    }
}

function showHideStartMenuPage()
{
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
    if (!isWin) return;

    // Hide the start menu selection if we're not installing the start menu shortcut
    var components = installer.components( ".+\\.startMenuShortcut$" );
    for (var i = 0; i < components.length; i++)
    {
        if ( components[i].installationRequested() ) {
            installer.setDefaultPageVisible(QInstaller.StartMenuSelection, true);
            return;
        }
    }
}

function addTargetDirWidget()
{
    if (targetDirectoryPage) return;

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

    if (!isWin) {
        targetDirectoryPage.RegisterFileCheckBox.hide();
    }
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
        targetDirectoryPage.warning.setText("<p style=\"color: #a526c4\">" + installer.value("Name") + " is already installed. <b>Clicking the <i>Next</i> button will automatically uninstall  it</b> before it's updated.</p>");

        doRunMaintenanceTool = true;

        /*installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, false);
        installer.setDefaultPageVisible(QInstaller.StartMenuSelection, false);
        installer.setDefaultPageVisible(QInstaller.PerformInstallation, false);
        installer.setDefaultPageVisible(QInstaller.LicenseCheck, false);
        installer.setDefaultPageVisible(QInstaller.ComponentSelection, false);

        targetDirectoryPage.RegisterFileCheckBox.hide();*/

        return;
    }

    doRunMaintenanceTool = false;

    /*if (installer.components().length > 2) installer.setDefaultPageVisible(QInstaller.ComponentSelection, true);

    installer.setDefaultPageVisible(QInstaller.ReadyForInstallation, true);
    installer.setDefaultPageVisible(QInstaller.StartMenuSelection, true);
    installer.setDefaultPageVisible(QInstaller.PerformInstallation, true);
    installer.setDefaultPageVisible(QInstaller.LicenseCheck, true);

    targetDirectoryPage.RegisterFileCheckBox.show();*/

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

    installer.gainAdminRights();

    var dir = installer.value("TargetDir");
    if (installer.fileExists(dir) && installer.fileExists(dir + "/" + maintenanceToolName)) {
        if (isMac)
            installer.execute(dir + "/" + maintenanceToolName + "/Contents/MacOS/" + maintenanceToolName.replace(".app", ""), /*["--start-uninstaller"]*/ ["purge", "-c"]);
        else
            installer.execute(dir + "/" + maintenanceToolName, /*["--start-uninstaller"]*/ ["purge", "-c"]);
    }
    else {
        QMessageBox.warning("maintenanceToolNotFound", "Maintenance Tool", "The Maintenance Tool can't be found.");
    }
    //gui.rejectWithoutPrompt();
}

function prepareInstallation()
{
    if (isWin) installer.setValue("registerFileType", targetDirectoryPage.RegisterFileCheckBox.checked);
    else installer.setValue("registerFileType", false);
}

function _a(text)
{
    QMessageBox.information(
        "debugAlert",
        "Installer Debug Alert",
        text.toString()
    );
}
