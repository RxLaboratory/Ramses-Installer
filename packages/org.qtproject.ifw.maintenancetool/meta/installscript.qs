function Component()
{
    installer.installationStarted.connect(this, Component.prototype.onInstallationStarted);
}

Component.prototype.onInstallationStarted = function()
{
    if (component.updateRequested() || component.installationRequested()) {
        if (installer.value("os") == "win") {
            component.installerbaseBinaryPath = "@TargetDir@/installerbase.exe";
        } else if (installer.value("os") == "x11") {
            component.installerbaseBinaryPath = "@TargetDir@/installerbase";
        } else if (installer.value("os") == "mac") {
            // In macOs maintenance tool can be either installerbase from Qt Installer
            // Framework's install folder, or app bundle created by binarycreator
            // with --create-maintenancetool switch. "MaintenanceTool.app" -name
            // may differ depending on what has been defined in config.xml while
            // creating the maintenance tool.
            // Use either of the following (not both):

            // component.installerbaseBinaryPath = "@TargetDir@/installerbase";
            component.installerbaseBinaryPath = "@TargetDir@/MaintenanceTool.app";
        }
        installer.setInstallerBaseBinary(component.installerbaseBinaryPath);

        var updateResourceFilePath = installer.value("TargetDir") + "/update.rcc";
        installer.setValue("DefaultResourceReplacement", updateResourceFilePath);
    }
}