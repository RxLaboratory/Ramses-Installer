/****************************************************************************
**
** Copyright (C) 2020 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the FOO module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:GPL-EXCEPT$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 as published by the Free Software
** Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

function Component()
{
    //We use the addRegisterFileCheckBox() function to display a check box for registering the generated file type on the last page of the installer. We hide the page when updating and uninstalling:
    component.loaded.connect(this, addRegisterFileCheckBox);
}

// called as soon as the component was loaded
addRegisterFileCheckBox = function()
{
    // don't show when updating or uninstalling
    if (installer.isInstaller()) {
        installer.addWizardPageItem(component, "RegisterFileCheckBoxForm", QInstaller.TargetDirectory);
    }
}

// here we are creating the operation chain which will be processed at the real installation part later
Component.prototype.createOperations = function()
{
    // call default implementation to actually install the registeredfile
    component.createOperations();

    if (component.userInterface("RegisterFileCheckBoxForm")) {
        var isRegisterFileChecked = component.userInterface("RegisterFileCheckBoxForm").RegisterFileCheckBox.checked;
    }
    if (systemInfo.productType === "windows" && isRegisterFileChecked) {
        var iconId = 0;
        var ramsesPath = installer.value("TargetDir") + "\\ramses.exe";
        component.addOperation("RegisterFileType",
                               "ramses",
                               ramsesPath + " '%1'",
                               "Ramses Database",
                               "application/x-sqlite3",
                               ramsesPath + "," + iconId,
                               "ProgId=org.rxlaboratory.ramses");
        component.addOperation("CreateShortcut",
                               "@TargetDir@/ramses.exe",
                               "@StartMenuDir@/Ramses.lnk",
                               "workingDirectory=@TargetDir@",
                               "iconPath=@TargetDir@/ramses.exe",
                               "iconId=0",
                               "description=Open Ramses");
    }
}
