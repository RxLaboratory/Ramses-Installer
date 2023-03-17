# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'finishWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_FinishWidget(object):
    def setupUi(self, FinishWidget):
        if not FinishWidget.objectName():
            FinishWidget.setObjectName(u"FinishWidget")
        FinishWidget.resize(504, 696)
        self.verticalLayout = QVBoxLayout(FinishWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 15, 0, 3)
        self.label = QLabel(FinishWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_5 = QLabel(FinishWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"margin-left: 20px;")
        self.label_5.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_5)

        self.widget = QWidget(FinishWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, -1, -1, -1)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.commercialButton = QRadioButton(self.widget)
        self.commercialButton.setObjectName(u"commercialButton")
        self.commercialButton.setChecked(True)

        self.verticalLayout_2.addWidget(self.commercialButton)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"margin-left: 20px; margin-bottom: 20px;")
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.nonProfitButton = QRadioButton(self.widget)
        self.nonProfitButton.setObjectName(u"nonProfitButton")

        self.verticalLayout_2.addWidget(self.nonProfitButton)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"margin-left: 20px;  margin-bottom: 20px;")
        self.label_4.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_4)

        self.membershipButton = QRadioButton(self.widget)
        self.membershipButton.setObjectName(u"membershipButton")

        self.verticalLayout_2.addWidget(self.membershipButton)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"margin-left: 20px;")
        self.label_2.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.giveAHandButton = QRadioButton(self.widget)
        self.giveAHandButton.setObjectName(u"giveAHandButton")

        self.verticalLayout_2.addWidget(self.giveAHandButton)

        self.dontWantButton = QRadioButton(self.widget)
        self.dontWantButton.setObjectName(u"dontWantButton")

        self.verticalLayout_2.addWidget(self.dontWantButton)

        self.okButton = QRadioButton(self.widget)
        self.okButton.setObjectName(u"okButton")

        self.verticalLayout_2.addWidget(self.okButton)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(FinishWidget)

        QMetaObject.connectSlotsByName(FinishWidget)
    # setupUi

    def retranslateUi(self, FinishWidget):
        FinishWidget.setWindowTitle(QCoreApplication.translate("FinishWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("FinishWidget", u"<strong>Your contribution</strong>", None))
        self.label_5.setText(QCoreApplication.translate("FinishWidget", u"<html><head/><body><p>The only way we can continue to develop, maintain, distribute and support free software is for you to contribute.</p><p>When making your donation, <span style=\" font-weight:700;\">you choose the amount, what you think is right, what you can afford</span>.</p></body></html>", None))
        self.commercialButton.setText(QCoreApplication.translate("FinishWidget", u"Commercial use", None))
        self.label_3.setText(QCoreApplication.translate("FinishWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">You\u2019re a company or a freelance professional</span>, you\u2019re being paid for your work, <span style=\" font-weight:700;\">you have to contribute before using our tools</span>.</p></body></html>", None))
        self.nonProfitButton.setText(QCoreApplication.translate("FinishWidget", u"Non-Profit / Educational use", None))
        self.label_4.setText(QCoreApplication.translate("FinishWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">You\u2019re a student or a teacher, you work for a non-profit organization, you\u2019re a hobbyist</span>, your donation is not mandatory but is still much needed.</p></body></html>", None))
        self.membershipButton.setText(QCoreApplication.translate("FinishWidget", u"RxLab Membership", None))
        self.label_2.setText(QCoreApplication.translate("FinishWidget", u"<html><head/><body><p><span style=\" font-weight:700;\">Support the development</span> of free and open source software by joining us, and get an <span style=\" font-weight:700;\">early access</span> to your shiny new <span style=\" font-weight:700;\">tools</span>, <span style=\" font-weight:700;\">tutorials</span> and other <span style=\" font-weight:700;\">exclusive perks</span>.</p></body></html>", None))
        self.giveAHandButton.setText(QCoreApplication.translate("FinishWidget", u"I'd rather give a hand than contribute financially", None))
        self.dontWantButton.setText(QCoreApplication.translate("FinishWidget", u"I don't want to contribute and support free and open source software.", None))
        self.okButton.setText(QCoreApplication.translate("FinishWidget", u"I've already contributed recently", None))
    # retranslateUi

