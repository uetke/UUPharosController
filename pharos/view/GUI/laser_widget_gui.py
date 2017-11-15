import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from lantz import Q_

class LaserWidgetGUI(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p,'QtCreator/laserwidget.ui'), self)

        self.status = {
            'LD_current': False,
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

        if values['sweep_mode'] in ('StepOne', 'StepTwo', 'StepOneTrig', 'StepTwoTrig'):
            self.step_line.setText(values['step'])
            self.step_time_line.setText(values['step_time'])

        self.start_wavelength_line.setText(values['start_wavelength'])
        self.stop_wavelength_line.setText(values['stop_wavelength'])
        self.speed_line.setText(values['wavelength_speed'])
        self.trigger_step_line.setText(values['interval_trigger'])

        if 'wait_time' in values:
            self.wait_line.setText(values['wait_time'])
        if 'number_sweeps' in values:
            self.sweeps_line.setText(str(values['number_sweeps']))

        if values['sweep_mode'] == 'ContOne':
            self.continuous_button.toggle()
            self.one_button.toggle()
        elif values['sweep_mode'] == 'ContTwo':
            self.continuous_button.toggle()
            self.two_button.toggle()
        elif values['sweep_mode'] == 'StepOne':
            self.step_button.toggle()
            self.one_button.toggle()
        elif values['sweep_mode'] == 'StepTwo':
            self.step_button.toggle()
            self.two_button.toggle()

        if values['timing_trigger'] == 'Step':
            self.trigger_step.toggle()
        elif values['timing_trigger'] == 'Start':
            self.trigger_start.toggle()
        elif values['timing_trigger'] == 'Stop':
            self.trigger_stop.toggle()

    def update_laser_values(self):
        values = {
            'start_wavelength': Q_(self.start_wavelength_line.text()),
            'stop_wavelength': Q_(self.stop_wavelength_line.text()),
            'wavelength_speed': Q_(self.speed_line.text()),
            'interval_trigger': Q_(self.trigger_step_line.text()),
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
            values.update({
                'step': Q_(self.step_line.text()),
                'step_time': Q_(self.step_time_line.text()),
            })
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

        if self.wait_line.text() != "":
            values.update({'wait': Q_(self.wait_line.text()), })
        if self.sweeps_line.text() != "":
            values.update({'wavelength_sweeps': self.sweeps_line.text(), })

        if self.trigger_step.isChecked():
            values['timing_trigger'] = 'Step'
        if self.trigger_start.isChecked():
            values['timing_trigger'] = 'Start'
        if self.trigger_stop.isChecked():
            values['timing_trigger'] = 'Stop'

        return values


if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    LW = LaserWidgetGUI()
    LW.show()
    sys.exit(app.exec_())
