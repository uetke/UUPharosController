from PyQt4 import QtCore
from .GUI.mainwindow import MainWindowGUI
from lantz import Q_
from lantz.ui.widgets import connect_feat
from time import sleep
import numpy as np

class MainWindow(MainWindowGUI):
    def __init__(self, session):
        MainWindowGUI.__init__(self, session.laser, parent=None)
        self.laser = session.laser
        self.daq = session.daq
        self.sesion = session

        QtCore.QObject.connect(self.laser_widget.start_button, QtCore.SIGNAL('clicked()'), self.start_monitor)

        #QtCore.QObject.connect(self.laser_widget.apply_button, QtCore.SIGNAL('clicked()'), self.update_laser)

    def update_laser(self):
        self.laser.wavelength = Q_(self.laser_widget.wavelength_line.text())
        self.laser.start_wavelength = Q_(self.laser_widget.start_wavelength_line.text())
        self.laser.stop_wavelength = Q_(self.laser_widget.stop_wavelength_line.text())
        self.laser.speed = Q_(self.laser_widget.speed_line.text())
        self.laser.trigger_step = Q_(self.laser_widget.trigger_step_line.text())
        self.laser.step = Q_(self.laser_widget.step_line.text())
        self.laser.power = Q_(self.laser_widget.power_line.text())
        self.laser.wait = Q_(self.laser_widget.wait_line.text())
        self.laser.step_time = Q_(self.laser_widget.step_time_line.text())
        self.laser.sweeps = Q_(self.laser_widget.sweeps_line.text())

    def start_monitor(self):
        self.update_laser()
        self.apply_monitor()
        
        if self.laser_widget.continuous_button.isChecked():
            if self.laser_widget.one_button.isChecked():
                if self.laser_widget.trigger_check.isChecked():
                    sweep_mode = 'ContOneTrig'
                else:
                    sweep_mode = 'ContOne'
            else:
                if self.laser_widget.trigger_check.isChecked():
                    sweep_mode = 'ContTwoTrig'
                else:
                    sweep_mode = 'ContTwo'
        else:
            if self.laser_widget.one_button.isChecked():
                if self.laser_widget.trigger_check.isChecked():
                    sweep_mode = 'StepOneTrig'
                else:
                    sweep_mode = 'StepOne'
            else:
                if self.laser_widget.trigger_check.isChecked():
                    sweep_mode = 'StepTwoTrig'
                else:
                    sweep_mode = 'StepTwo'
        print('Sweep mode: '+sweep_mode)
        self.laser.sweep_mode = sweep_mode
        points = int((self.laser.stop_wavelength-self.laser.start_wavelength)/self.laser.trigger_step)
        wavelength = np.linspace(self.laser.start_wavelength, self.laser.stop_wavelength, points)
        for dev in self.devs_to_monitor:
            print(dev.properties)
            monit = self.monitor[dev.properties['name']]
            monit['widget'].main_plot.setLabel('bottom', 'Wavelength', units='nm')
            monit['widget'].main_plot.showGrid(True, True)
            monit['dataX'] = wavelength
        
        print('Point: %s' % points)
        accuracy = self.laser.trigger_step/self.laser.speed
        conditions = {'devices': self.devs_to_monitor,
                      'accuracy': accuracy,
                      'trigger': 'external',
                      'trigger_source': 'PFI0',
                      'points': points}

        task = self.daq.analog_input_setup(conditions)
        self.daq.trigger_analog(task)
        self.laser.execute_sweep()
        # self.laser.software_trigger()
        while not self.laser.sweep_condition == 'Stop':
            print('Waiting for laser')
            sleep(0.5)

        conditions['points'] = -1
        v, d = self.daq.read_analog(task, conditions)
        for a in d:
            print(a)
        print('Sweep Finished')

if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    import sys
    from model.lib.session import session
    session.laser = None
    session.adq = None

    ap = QApplication(sys.argv)
    window = MainWindow(session)
    window.show()
    ap.exit(ap.exec_())