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


    def populate_values(self, values):
        """
        :param values: needs to have all the attributes to populate the values displayed
        :return:
        """
        self.start_wavelength_line.setText(values['start_wavelength'])
        self.stop_wavelength_line.setText(values['stop_wavelength'])
        self.speed_line.setText(values['wavelength_speed'])
        #self.step_line.setText(values['step'])
        self.trigger_step_line.setText(values['trigger_step'])
        #self.wait_line.setText(values['wait_time'])
        #self.step_time_line.setText(values['step_time'])
        #self.sweeps_line.setText(str(values['number_sweeps']))

        #if values['sweep'] == 'continuous':
        #    self.continuous_button.toggle()
        #elif values['sweep'] == 'step':
        #    self.step_button.toggle()
        #
        #if values['mode'] == 'one':
        #    self.one_button.toggle()
        #elif values['mode'] == 'two':
        #    self.two_button.toggle()
        #
        #self.trigger_check.setChecked(values['trigger'])

    def update_laser_values(self):
        values = {
            'start_wavelength': Q_(self.start_wavelength_line.text()),
            'stop_wavelength': Q_(self.stop_wavelength_line.text()),
            'speed': Q_(self.speed_line.text()),
            'trigger_step': Q_(self.trigger_step_line.text()),
            'step ': Q_(self.step_line.text()),
            'wait': Q_(self.wait_line.text()),
            'step_time': Q_(self.step_time_line.text()),
            'sweeps': Q_(self.sweeps_line.text()),
          }
        if self.continuous_button.isChecked():
            if self.one_button.isChecked():
                if self.trigger_check.isChecked():
                    sweep_mode = 'ContOneTrig'
                else:
                    sweep_mode = 'ContOne'
            else:
                if self.trigger_check.isChecked():
                    sweep_mode = 'ContTwoTrig'
                else:
                    sweep_mode = 'ContTwo'
        else:
            if self.one_button.isChecked():
                if self.trigger_check.isChecked():
                    sweep_mode = 'StepOneTrig'
                else:
                    sweep_mode = 'StepOne'
            else:
                if self.trigger_check.isChecked():
                    sweep_mode = 'StepTwoTrig'
                else:
                    sweep_mode = 'StepTwo'
        values['sweep_mode'] = sweep_mode

        return values


if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    LW = LaserWidgetGUI()
    LW.show()
    sys.exit(app.exec_())
