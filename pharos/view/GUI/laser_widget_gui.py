import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from lantz import Q_

class LaserWidgetGUI(QtGui.QWidget):
    button_pressed_signal = QtCore.pyqtSignal([bool], ['QString'], name='button_pressed')

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p,'QtCreator/laserwidget.ui'), self)

        self.status = {'LD_current': False,
                       'auto_power': False,
                       'coherent_control': False,
                       'shutter': False,
                       'trigger': False,
        }

        QtCore.QObject.connect(self.LD_current, QtCore.SIGNAL('clicked()'), self.set_param_button)
        QtCore.QObject.connect(self.auto_power, QtCore.SIGNAL('clicked()'), self.set_param_button)
        QtCore.QObject.connect(self.coherent_control, QtCore.SIGNAL('clicked()'), self.set_param_button)
        QtCore.QObject.connect(self.shutter, QtCore.SIGNAL('clicked()'), self.set_param_button)
        QtCore.QObject.connect(self.trigger, QtCore.SIGNAL('clicked()'), self.set_param_button)

    def populate_values(self, values):
        """
        :param values: needs to have all the attributes to populate the values displayed
        :return:
        """
        self.wavelength_line.setText(values['wavelength'])
        self.start_wavelength_line.setText(values['start_wavelength'])
        self.stop_wavelength_line.setText(values['stop_wavelength'])
        self.power_line.setText(values['stop_wavelength'])
        self.speed_line.setText(values['speed'])
        self.step_line.setText(values['step'])
        self.trigger_step_line.setText(values['trigger_step'])
        self.wait_line.setText(values['wait'])
        self.step_time_line.setText(values['step_time'])
        self.sweeps_line.setText(str(values['sweeps']))
        self.power_line.setText(values['power'])
        p = int(values['power'].split(' ')[0]) * 100

        if values['sweep'] == 'continuous':
            self.continuous_button.toggle()
        elif values['sweep'] == 'step':
            self.step_button.toggle()

        if values['mode'] == 'one':
            self.one_button.toggle()
        elif values['mode'] == 'two':
            self.two_button.toggle()

        self.trigger_check.setChecked(values['trigger'])

    def set_param_button(self):
        self.status[self.sender().objectName()] = not self.status[self.sender().objectName()]
        for s in self.status:
            button = getattr(self, s)
            button.setDown(self.status[s])

        self.emit(QtCore.SIGNAL('button_pressed'), self.status[self.sender().objectName()], self.sender().objectName() )

    def update_laser(self):
        values = {
            'wavelength': Q_(self.laser_widget.wavelength_line.text()),
            'start_wavelength': Q_(self.laser_widget.start_wavelength_line.text()),
            'stop_wavelength': Q_(self.laser_widget.stop_wavelength_line.text()),
            'speed': Q_(self.laser_widget.speed_line.text()),
            'trigger_step': Q_(self.laser_widget.trigger_step_line.text()),
            'step ': Q_(self.laser_widget.step_line.text()),
            'power': Q_(self.laser_widget.power_line.text()),
            'wait': Q_(self.laser_widget.wait_line.text()),
            'step_time': Q_(self.laser_widget.step_time_line.text()),
            'sweeps': Q_(self.laser_widget.sweeps_line.text()),
          }
        self.emit(QtCore.SIGNAL('values_updated'), values)
        return values


if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    LW = LaserWidgetGUI()
    LW.show()
    sys.exit(app.exec_())
