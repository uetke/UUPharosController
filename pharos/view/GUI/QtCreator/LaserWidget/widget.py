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
        Form.resize(354, 432)
        self.gridLayout_4 = QtGui.QGridLayout(Form)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.auto_power_button = QtGui.QPushButton(Form)
        self.auto_power_button.setObjectName(_fromUtf8("auto_power_button"))
        self.gridLayout_4.addWidget(self.auto_power_button, 9, 0, 1, 1)
        self.step_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.step_label.setFont(font)
        self.step_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.step_label.setObjectName(_fromUtf8("step_label"))
        self.gridLayout_4.addWidget(self.step_label, 6, 0, 1, 1)
        self.start_wavelength_line = QtGui.QLineEdit(Form)
        self.start_wavelength_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.start_wavelength_line.setFont(font)
        self.start_wavelength_line.setObjectName(_fromUtf8("start_wavelength_line"))
        self.gridLayout_4.addWidget(self.start_wavelength_line, 2, 1, 1, 1)
        self.trigger_step_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trigger_step_label.setFont(font)
        self.trigger_step_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.trigger_step_label.setObjectName(_fromUtf8("trigger_step_label"))
        self.gridLayout_4.addWidget(self.trigger_step_label, 5, 0, 1, 1)
        self.speed_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.speed_label.setFont(font)
        self.speed_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.speed_label.setObjectName(_fromUtf8("speed_label"))
        self.gridLayout_4.addWidget(self.speed_label, 4, 0, 1, 1)
        self.condition_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.condition_label.setFont(font)
        self.condition_label.setObjectName(_fromUtf8("condition_label"))
        self.gridLayout_4.addWidget(self.condition_label, 11, 0, 1, 2)
        self.stop_wavelength_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.stop_wavelength_label.setFont(font)
        self.stop_wavelength_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stop_wavelength_label.setObjectName(_fromUtf8("stop_wavelength_label"))
        self.gridLayout_4.addWidget(self.stop_wavelength_label, 3, 0, 1, 1)
        self.wavelength_line = QtGui.QLineEdit(Form)
        self.wavelength_line.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wavelength_line.sizePolicy().hasHeightForWidth())
        self.wavelength_line.setSizePolicy(sizePolicy)
        self.wavelength_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.wavelength_line.setFont(font)
        self.wavelength_line.setAutoFillBackground(False)
        self.wavelength_line.setObjectName(_fromUtf8("wavelength_line"))
        self.gridLayout_4.addWidget(self.wavelength_line, 0, 1, 1, 1)
        self.LD_button = QtGui.QPushButton(Form)
        self.LD_button.setObjectName(_fromUtf8("LD_button"))
        self.gridLayout_4.addWidget(self.LD_button, 8, 0, 1, 1)
        self.start_wavelength_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.start_wavelength_label.setFont(font)
        self.start_wavelength_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.start_wavelength_label.setObjectName(_fromUtf8("start_wavelength_label"))
        self.gridLayout_4.addWidget(self.start_wavelength_label, 2, 0, 1, 1)
        self.coherent_button = QtGui.QPushButton(Form)
        self.coherent_button.setObjectName(_fromUtf8("coherent_button"))
        self.gridLayout_4.addWidget(self.coherent_button, 10, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.continuous_button = QtGui.QRadioButton(self.groupBox)
        self.continuous_button.setObjectName(_fromUtf8("continuous_button"))
        self.gridLayout.addWidget(self.continuous_button, 0, 0, 1, 1)
        self.step_button = QtGui.QRadioButton(self.groupBox)
        self.step_button.setObjectName(_fromUtf8("step_button"))
        self.gridLayout.addWidget(self.step_button, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.one_button = QtGui.QRadioButton(self.groupBox_2)
        self.one_button.setObjectName(_fromUtf8("one_button"))
        self.gridLayout_2.addWidget(self.one_button, 0, 0, 1, 1)
        self.two_button = QtGui.QRadioButton(self.groupBox_2)
        self.two_button.setObjectName(_fromUtf8("two_button"))
        self.gridLayout_2.addWidget(self.two_button, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.trigger_check = QtGui.QCheckBox(self.groupBox_3)
        self.trigger_check.setObjectName(_fromUtf8("trigger_check"))
        self.gridLayout_3.addWidget(self.trigger_check, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.gridLayout_4.addLayout(self.horizontalLayout, 7, 0, 1, 4)
        self.wavelength_labe = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.wavelength_labe.setFont(font)
        self.wavelength_labe.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.wavelength_labe.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.wavelength_labe.setObjectName(_fromUtf8("wavelength_labe"))
        self.gridLayout_4.addWidget(self.wavelength_labe, 0, 0, 1, 1)
        self.stop_wavelength_line = QtGui.QLineEdit(Form)
        self.stop_wavelength_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.stop_wavelength_line.setFont(font)
        self.stop_wavelength_line.setObjectName(_fromUtf8("stop_wavelength_line"))
        self.gridLayout_4.addWidget(self.stop_wavelength_line, 3, 1, 1, 1)
        self.speed_line = QtGui.QLineEdit(Form)
        self.speed_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.speed_line.setFont(font)
        self.speed_line.setObjectName(_fromUtf8("speed_line"))
        self.gridLayout_4.addWidget(self.speed_line, 4, 1, 1, 1)
        self.trigger_step_line = QtGui.QLineEdit(Form)
        self.trigger_step_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.trigger_step_line.setFont(font)
        self.trigger_step_line.setObjectName(_fromUtf8("trigger_step_line"))
        self.gridLayout_4.addWidget(self.trigger_step_line, 5, 1, 1, 1)
        self.step_line = QtGui.QLineEdit(Form)
        self.step_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.step_line.setFont(font)
        self.step_line.setText(_fromUtf8(""))
        self.step_line.setObjectName(_fromUtf8("step_line"))
        self.gridLayout_4.addWidget(self.step_line, 6, 1, 1, 1)
        self.power_line = QtGui.QLineEdit(Form)
        self.power_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.power_line.setFont(font)
        self.power_line.setObjectName(_fromUtf8("power_line"))
        self.gridLayout_4.addWidget(self.power_line, 0, 2, 1, 1)
        self.power_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.power_label.setFont(font)
        self.power_label.setObjectName(_fromUtf8("power_label"))
        self.gridLayout_4.addWidget(self.power_label, 0, 3, 1, 1)
        self.steps_line = QtGui.QLineEdit(Form)
        self.steps_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.steps_line.setFont(font)
        self.steps_line.setObjectName(_fromUtf8("steps_line"))
        self.gridLayout_4.addWidget(self.steps_line, 2, 2, 1, 1)
        self.wait_line = QtGui.QLineEdit(Form)
        self.wait_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.wait_line.setFont(font)
        self.wait_line.setObjectName(_fromUtf8("wait_line"))
        self.gridLayout_4.addWidget(self.wait_line, 3, 2, 1, 1)
        self.step_time_line = QtGui.QLineEdit(Form)
        self.step_time_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.step_time_line.setFont(font)
        self.step_time_line.setObjectName(_fromUtf8("step_time_line"))
        self.gridLayout_4.addWidget(self.step_time_line, 4, 2, 1, 1)
        self.sweeps_line = QtGui.QLineEdit(Form)
        self.sweeps_line.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.sweeps_line.setFont(font)
        self.sweeps_line.setObjectName(_fromUtf8("sweeps_line"))
        self.gridLayout_4.addWidget(self.sweeps_line, 5, 2, 1, 1)
        self.steps_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.steps_label.setFont(font)
        self.steps_label.setObjectName(_fromUtf8("steps_label"))
        self.gridLayout_4.addWidget(self.steps_label, 2, 3, 1, 1)
        self.wait_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.wait_label.setFont(font)
        self.wait_label.setObjectName(_fromUtf8("wait_label"))
        self.gridLayout_4.addWidget(self.wait_label, 3, 3, 1, 1)
        self.step_time_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.step_time_label.setFont(font)
        self.step_time_label.setObjectName(_fromUtf8("step_time_label"))
        self.gridLayout_4.addWidget(self.step_time_label, 4, 3, 1, 1)
        self.sweeps_label = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.sweeps_label.setFont(font)
        self.sweeps_label.setObjectName(_fromUtf8("sweeps_label"))
        self.gridLayout_4.addWidget(self.sweeps_label, 5, 3, 1, 1)
        self.fine_tune_button = QtGui.QPushButton(Form)
        self.fine_tune_button.setObjectName(_fromUtf8("fine_tune_button"))
        self.gridLayout_4.addWidget(self.fine_tune_button, 8, 1, 1, 1)
        self.shutter_button = QtGui.QPushButton(Form)
        self.shutter_button.setObjectName(_fromUtf8("shutter_button"))
        self.gridLayout_4.addWidget(self.shutter_button, 9, 1, 1, 1)
        self.trigger_output_button = QtGui.QPushButton(Form)
        self.trigger_output_button.setObjectName(_fromUtf8("trigger_output_button"))
        self.gridLayout_4.addWidget(self.trigger_output_button, 10, 1, 1, 1)
        self.start_button = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.start_button.setFont(font)
        self.start_button.setAutoFillBackground(True)
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.gridLayout_4.addWidget(self.start_button, 8, 2, 1, 2)
        self.pause_button = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pause_button.setFont(font)
        self.pause_button.setObjectName(_fromUtf8("pause_button"))
        self.gridLayout_4.addWidget(self.pause_button, 9, 2, 1, 2)
        self.stop_button = QtGui.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName(_fromUtf8("stop_button"))
        self.gridLayout_4.addWidget(self.stop_button, 10, 2, 1, 2)
        self.step_label.setBuddy(self.step_line)
        self.trigger_step_label.setBuddy(self.trigger_step_line)
        self.speed_label.setBuddy(self.speed_line)
        self.stop_wavelength_label.setBuddy(self.stop_wavelength_line)
        self.start_wavelength_label.setBuddy(self.start_wavelength_line)
        self.wavelength_labe.setBuddy(self.wavelength_line)
        self.power_label.setBuddy(self.power_line)
        self.steps_label.setBuddy(self.steps_line)
        self.wait_label.setBuddy(self.wait_line)
        self.step_time_label.setBuddy(self.step_time_line)
        self.sweeps_label.setBuddy(self.sweeps_line)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.continuous_button, self.step_button)
        Form.setTabOrder(self.step_button, self.one_button)
        Form.setTabOrder(self.one_button, self.two_button)
        Form.setTabOrder(self.two_button, self.trigger_check)
        Form.setTabOrder(self.trigger_check, self.LD_button)
        Form.setTabOrder(self.LD_button, self.auto_power_button)
        Form.setTabOrder(self.auto_power_button, self.coherent_button)
        Form.setTabOrder(self.coherent_button, self.pause_button)
        Form.setTabOrder(self.pause_button, self.stop_button)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.auto_power_button.setText(_translate("Form", "Auto Power", None))
        self.step_label.setText(_translate("Form", "Step", None))
        self.trigger_step_label.setText(_translate("Form", "Trig. Step", None))
        self.speed_label.setText(_translate("Form", "Speed", None))
        self.condition_label.setText(_translate("Form", "Current condition:", None))
        self.stop_wavelength_label.setText(_translate("Form", "Stop", None))
        self.LD_button.setText(_translate("Form", "LD Current", None))
        self.start_wavelength_label.setText(_translate("Form", "Start", None))
        self.coherent_button.setText(_translate("Form", "Coherent", None))
        self.groupBox.setTitle(_translate("Form", "Sweep", None))
        self.continuous_button.setText(_translate("Form", "Continuous", None))
        self.step_button.setText(_translate("Form", "Step", None))
        self.groupBox_2.setTitle(_translate("Form", "Mode", None))
        self.one_button.setText(_translate("Form", "One-way", None))
        self.two_button.setText(_translate("Form", "Two-way", None))
        self.groupBox_3.setTitle(_translate("Form", "Trigger", None))
        self.trigger_check.setText(_translate("Form", "Ext. Trigger", None))
        self.wavelength_labe.setText(_translate("Form", "Wavelength", None))
        self.power_label.setText(_translate("Form", "Power", None))
        self.steps_label.setText(_translate("Form", "# Steps", None))
        self.wait_label.setText(_translate("Form", "Wait Time", None))
        self.step_time_label.setText(_translate("Form", "Step Time", None))
        self.sweeps_label.setText(_translate("Form", "# Sweeps", None))
        self.fine_tune_button.setText(_translate("Form", "Fine Tune", None))
        self.shutter_button.setText(_translate("Form", "Shutter", None))
        self.trigger_output_button.setText(_translate("Form", "Trigger", None))
        self.start_button.setText(_translate("Form", "Start", None))
        self.pause_button.setText(_translate("Form", "Pause", None))
        self.stop_button.setText(_translate("Form", "Stop", None))

