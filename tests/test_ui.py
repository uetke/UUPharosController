import os
import sys
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_
from PyQt4.Qt import QApplication
import pharos.view.GUI.QtCreator.resources_rc
from pharos.view.GUI.laser_widget import LaserWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        p = os.path.dirname(__file__).split('/')
        uic.loadUi(os.path.join('C:\\Users\\Aquiles\\Documents\\Programs\\PharosController\\', 'pharos\\view\\GUI\\QtCreator\main_window.ui'), self)

        # Make connections
        QtCore.QObject.connect(self.apply_laser, QtCore.SIGNAL('clicked()'), self.update_laser)
        # QtCore.QObject.connect(self.laser_button, QtCore.SIGNAL('clicked()'), self.laser_widget.show)
        # QtCore.QObject.connect(self.monitor_button, QtCore.SIGNAL('clicked()'), self.monitor_widget.show)
        QtCore.QObject.connect(self.wavelength_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_wavelength)
        QtCore.QObject.connect(self.power_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_power)
        QtCore.QObject.connect(self.shutter, QtCore.SIGNAL('stateChanged(int)'), self.update_shutter)

    def update_laser(self):
        wavelength = Q_(self.wavelength.text())
        power = Q_(self.power.text())
        values = {
            'wavelength': wavelength,
            'powermW': power,
        }
        self.wavelength_slider.setValue((wavelength.m_as(Q_('nm')) - 1480) / 0.0001)
        print(values)

    def update_wavelength(self, value):
        new_value = 1480+value*0.0001
        new_value = new_value*Q_('nm')
        self.wavelength.setText('{:~}'.format(new_value))
        print(new_value)

    def update_shutter(self, state):
        state = bool(state)
        #self.shutter_value = not self.shutter_value
        print(state)
        # self.shutter.setDown(self.shutter_value)

    def update_power(self, value):
        new_value = 0.01+value*0.01
        new_value = new_value*Q_('mW')
        self.power.setText('{:~}'.format(new_value))
        print(new_value)

ap = QApplication(sys.argv)
m = MainWindow()
m.show()
ap.exit(ap.exec_())