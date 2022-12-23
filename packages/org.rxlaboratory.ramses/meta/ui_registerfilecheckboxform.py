# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registerfilecheckboxform.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RegisterFileCheckBoxForm(object):
    def setupUi(self, RegisterFileCheckBoxForm):
        if not RegisterFileCheckBoxForm.objectName():
            RegisterFileCheckBoxForm.setObjectName(u"RegisterFileCheckBoxForm")
        RegisterFileCheckBoxForm.resize(400, 300)
        self.verticalLayout = QVBoxLayout(RegisterFileCheckBoxForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.RegisterFileCheckBox = QCheckBox(RegisterFileCheckBoxForm)
        self.RegisterFileCheckBox.setObjectName(u"RegisterFileCheckBox")
        self.RegisterFileCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.RegisterFileCheckBox)


        self.retranslateUi(RegisterFileCheckBoxForm)

        QMetaObject.connectSlotsByName(RegisterFileCheckBoxForm)
    # setupUi

    def retranslateUi(self, RegisterFileCheckBoxForm):
        RegisterFileCheckBoxForm.setWindowTitle(QCoreApplication.translate("RegisterFileCheckBoxForm", u"Form", None))
        self.RegisterFileCheckBox.setText(QCoreApplication.translate("RegisterFileCheckBoxForm", u"Associate *.ramses files with the Ramses Application", None))
    # retranslateUi

