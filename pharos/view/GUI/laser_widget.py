import sys
import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from lantz.ui.widgets import connect_feat

class LaserWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p,'QtCreator/laserwidget.ui'), self)

        self.LD_current = False
        self.auto_power = False
        self.coherent = False
        self.fine_tune = False
        self.shutter = False
        self.trigger = False

        QtCore.QObject.connect(self.LD_button,QtCore.SIGNAL('clicked()'), self.set_LD_current)
        QtCore.QObject.connect(self.auto_power_button, QtCore.SIGNAL('clicked()'), self.set_auto_power)
        QtCore.QObject.connect(self.coherent_button, QtCore.SIGNAL('clicked()'), self.set_coherent)
        QtCore.QObject.connect(self.trigger_button, QtCore.SIGNAL('clicked()'), self.set_trigger)
        
    def set_LD_current(self):
        self.LD_current = not self.LD_current
        self.LD_button.setDown(self.LD_current)
        self.laser.LD_current = self.LD_current

    def set_auto_power(self):
        self.auto_power = not self.auto_power
        self.auto_power_button.setDown(self.auto_power)
        self.laser.auto_power = self.auto_power

    def set_coherent(self):
        self.coherent = not self.coherent
        self.coherent_button.setDown(self.coherent)
        self.laser.coherent_control = self.coherent

    def set_trigger(self):
        self.trigger = not self.trigger
        self.trigger_button.setDown(self.trigger)
        self.laser.trigger = self.trigger

    def connect_laser(self, laser):
        self.laser = laser

    def populate_values(self, dict):
        """
        :param dict: needs to have all the attributes to populate the values displayed
        :return:
        """
        self.wavelength_line.setText(dict['wavelength'])
        self.start_wavelength_line.setText(dict['start_wavelength'])
        self.stop_wavelength_line.setText(dict['stop_wavelength'])
        self.power_line.setText(dict['stop_wavelength'])
        self.speed_line.setText(dict['speed'])
        self.steps_line.setText(str(dict['steps']))
        self.step_line.setText(dict['step'])
        self.trigger_step_line.setText(dict['trigger_step'])
        self.wait_line.setText(dict['wait'])
        self.step_time_line.setText(dict['step_time'])
        self.sweeps_line.setText(str(dict['sweeps']))
        self.power_line.setText(dict['power'])
        p = int(dict['power'].split(' ')[0])*100

        if dict['sweep'] == 'continuous':
            self.continuous_button.toggle()
        elif dict['sweep'] == 'step':
            self.step_button.toggle()

        if dict['mode'] == 'one':
            self.one_button.toggle()
        elif dict['mode'] == 'two':
            self.two_button.toggle()

        self.trigger_check.setChecked(dict['trigger'])
        self.LD_button.setDown(dict['LD'])
        self.auto_power_button.setDown(dict['auto_power'])
        self.coherent_button.setDown(dict['coherent'])
        self.fine_tune_button.setDown(dict['fine_tune'])
        self.shutter_button.setDown(dict['shutter'])
        self.trigger_output_button.setDown(dict['trigger_output'])



if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    mon = LaserWidget()
    mon.show()
    sys.exit(app.exec_())
