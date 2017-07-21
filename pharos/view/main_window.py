import numpy as np
import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_
from lantz.ui.widgets import WidgetMixin

from pharos.view.GUI.laser_widget import LaserWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget


class MainWindow(QtGui.QMainWindow):
    def __init__(self, session, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/QtCreator/main_window.ui'), self)
        self.session = session

        # Load Widgets
        # self.laser_widget = LaserWidget(self.session.laser)
        self.monitor_widget = MonitorConfigWidget()
        # widget_test = WidgetMixin.from_feat(self.session.laser.driver.wavelength)
        # self.Bottom_Layout.addwidget(widget_test)
        # Make connections
        QtCore.QObject.connect(self.apply_laser, QtCore.SIGNAL('clicked()'), self.update_laser)
        #QtCore.QObject.connect(self.laser_button, QtCore.SIGNAL('clicked()'), self.laser_widget.show)
        QtCore.QObject.connect(self.monitor_button, QtCore.SIGNAL('clicked()'), self.monitor_widget.show)
        self.wavelength_slider.valueChanged.connect(self.update_wavelength)

    def update_laser(self):
        wavelength = Q_(self.wavelength.text())
        power = Q_(self.power.text())
        values = {
            'wavelength': wavelength,
            'power': power,
        }
        print(values)
        # self.session.laser.apply_values(values)

    def update_wavelength(self, value):
        print(value)
        print(self.wavelength_slider.value())