# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'targetWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TargetDirWidget(object):
    def setupUi(self, TargetWidget):
        if not TargetWidget.objectName():
            TargetWidget.setObjectName(u"TargetWidget")
        TargetWidget.resize(560, 264)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TargetWidget.sizePolicy().hasHeightForWidth())
        TargetWidget.setSizePolicy(sizePolicy)
        TargetWidget.setMinimumSize(QSize(491, 190))
        self.verticalLayout = QVBoxLayout(TargetWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.description = QLabel(TargetWidget)
        self.description.setObjectName(u"description")

        self.verticalLayout.addWidget(self.description)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.targetDirectory = QLineEdit(TargetWidget)
        self.targetDirectory.setObjectName(u"targetDirectory")
        self.targetDirectory.setReadOnly(True)

        self.horizontalLayout.addWidget(self.targetDirectory)

        self.targetChooser = QToolButton(TargetWidget)
        self.targetChooser.setObjectName(u"targetChooser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.targetChooser.sizePolicy().hasHeightForWidth())
        self.targetChooser.setSizePolicy(sizePolicy1)
        self.targetChooser.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.targetChooser)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.warning = QLabel(TargetWidget)
        self.warning.setObjectName(u"warning")
        self.warning.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.warning)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.RegisterFileCheckBox = QCheckBox(TargetWidget)
        self.RegisterFileCheckBox.setObjectName(u"RegisterFileCheckBox")
        self.RegisterFileCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.RegisterFileCheckBox)

        self.AddStartMenuShortcutCheckBox = QCheckBox(TargetWidget)
        self.AddStartMenuShortcutCheckBox.setObjectName(u"AddStartMenuShortcutCheckBox")
        self.AddStartMenuShortcutCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.AddStartMenuShortcutCheckBox)

        self.AddDesktopShortcutCheckBox = QCheckBox(TargetWidget)
        self.AddDesktopShortcutCheckBox.setObjectName(u"AddDesktopShortcutCheckBox")
        self.AddDesktopShortcutCheckBox.setChecked(False)

        self.verticalLayout.addWidget(self.AddDesktopShortcutCheckBox)

        self.verticalSpacer = QSpacerItem(20, 122, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(TargetWidget)

        QMetaObject.connectSlotsByName(TargetWidget)
    # setupUi

    def retranslateUi(self, TargetWidget):
        TargetWidget.setWindowTitle(QCoreApplication.translate("TargetDirWidget", u"Form", None))
        self.description.setText("")
        self.targetChooser.setText(QCoreApplication.translate("TargetDirWidget", u"...", None))
        self.warning.setText(QCoreApplication.translate("TargetDirWidget", u"TextLabel", None))
        self.RegisterFileCheckBox.setText(QCoreApplication.translate("TargetDirWidget", u"Associate *.ramses files with the Ramses Application", None))
        self.AddStartMenuShortcutCheckBox.setText(QCoreApplication.translate("TargetDirWidget", u"Create start menu entry", None))
        self.AddDesktopShortcutCheckBox.setText(QCoreApplication.translate("TargetDirWidget", u"Create desktop shortcut", None))
    # retranslateUi

