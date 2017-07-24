# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\monitor_config.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(369, 428)
        self.trigger = QtGui.QComboBox(Form)
        self.trigger.setGeometry(QtCore.QRect(67, 9, 82, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trigger.setFont(font)
        self.trigger.setObjectName(_fromUtf8("trigger"))
        self.trigger.addItem(_fromUtf8(""))
        self.trigger.addItem(_fromUtf8(""))
        self.trigger_label = QtGui.QLabel(Form)
        self.trigger_label.setGeometry(QtCore.QRect(9, 9, 52, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trigger_label.setFont(font)
        self.trigger_label.setObjectName(_fromUtf8("trigger_label"))
        self.devices_widget = QtGui.QWidget(Form)
        self.devices_widget.setGeometry(QtCore.QRect(9, 40, 351, 331))
        self.devices_widget.setObjectName(_fromUtf8("devices_widget"))
        self.trigger_info = QtGui.QLineEdit(Form)
        self.trigger_info.setGeometry(QtCore.QRect(155, 9, 167, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.trigger_info.setFont(font)
        self.trigger_info.setObjectName(_fromUtf8("trigger_info"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(331, 9, 29, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 390, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 390, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.trigger_label.setBuddy(self.trigger)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Monitor Configuration", None))
        self.trigger.setItemText(0, _translate("Form", "External", None))
        self.trigger.setItemText(1, _translate("Form", "Internal", None))
        self.trigger_label.setText(_translate("Form", "Trigger", None))
        self.label.setText(_translate("Form", "Port", None))
        self.pushButton.setText(_translate("Form", "Select all", None))
        self.pushButton_2.setText(_translate("Form", "Start", None))

