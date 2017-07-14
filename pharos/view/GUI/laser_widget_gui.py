import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui

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
        #self.LD_button.setDown(dict['LD'])
        #self.auto_power_button.setDown(dict['auto_power'])
        #self.coherent_button.setDown(dict['coherent'])
        #self.fine_tune_button.setDown(dict['fine_tune'])
        #self.shutter_button.setDown(dict['shutter'])
        #self.trigger_output_button.setDown(dict['trigger_output'])

    def set_param_button(self):
        self.status[self.sender().objectName()] = not self.status[self.sender().objectName()]
        for s in self.status:
            button = getattr(self, s)
            button.setDown(self.status[s])

        self.emit(QtCore.SIGNAL('button_pressed'), self.status[self.sender().objectName()], self.sender().objectName() )

if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    LW = LaserWidgetGUI()
    LW.show()
    sys.exit(app.exec_())
