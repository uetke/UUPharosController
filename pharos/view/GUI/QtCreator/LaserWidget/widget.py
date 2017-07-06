# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\laserwidget.ui'
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
        Form.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.stop_line = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.stop_line.setFont(font)
        self.stop_line.setObjectName(_fromUtf8("stop_line"))
        self.gridLayout.addWidget(self.stop_line, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.start_line = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.start_line.setFont(font)
        self.start_line.setObjectName(_fromUtf8("start_line"))
        self.gridLayout.addWidget(self.start_line, 1, 1, 1, 1)
        self.mode_combo = QtGui.QComboBox(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.mode_combo.setFont(font)
        self.mode_combo.setObjectName(_fromUtf8("mode_combo"))
        self.gridLayout.addWidget(self.mode_combo, 4, 1, 1, 1)
        self.speed_line = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.speed_line.setFont(font)
        self.speed_line.setObjectName(_fromUtf8("speed_line"))
        self.gridLayout.addWidget(self.speed_line, 3, 1, 1, 1)
        self.wavelength_line = QtGui.QLineEdit(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.wavelength_line.setFont(font)
        self.wavelength_line.setObjectName(_fromUtf8("wavelength_line"))
        self.gridLayout.addWidget(self.wavelength_line, 0, 1, 1, 1)
        self.power_slider = QtGui.QSlider(Form)
        self.power_slider.setMinimum(1)
        self.power_slider.setMaximum(10000)
        self.power_slider.setOrientation(QtCore.Qt.Vertical)
        self.power_slider.setObjectName(_fromUtf8("power_slider"))
        self.gridLayout.addWidget(self.power_slider, 0, 2, 5, 1)
        self.label_4.setBuddy(self.speed_line)
        self.label_2.setBuddy(self.start_line)
        self.label_5.setBuddy(self.mode_combo)
        self.label.setBuddy(self.wavelength_line)
        self.label_3.setBuddy(self.stop_line)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_4.setText(_translate("Form", "Speed", None))
        self.label_2.setText(_translate("Form", "Start", None))
        self.label_5.setText(_translate("Form", "Mode", None))
        self.label.setText(_translate("Form", "Wavelength", None))
        self.label_3.setText(_translate("Form", "Stop", None))

