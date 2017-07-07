import sys

from pyqtgraph.Qt import QtGui
from .QtCreator.LaserWidget.widget import Ui_Form

class LaserWidget(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        #self.ui = Ui_Form()
        self.setupUi(self)

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
        self.wait_line.setText(dict['wait'])
        self.step_time_line.setText(dict['step_time'])
        self.sweeps_line.setText(str(dict['sweeps']))
        self.power_line.setText(dict['power'])
        p = int(dict['power'].split(' ')[0])*100
        self.power_slider.setValue(p)

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
