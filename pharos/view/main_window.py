from PyQt4 import QtCore
from .GUI.mainwindow import MainWindowGUI
from lantz import Q_
from lantz.ui.widgets import connect_feat
from time import sleep

class MainWindow(MainWindowGUI):
    def __init__(self, session):
        MainWindowGUI.__init__(self, parent=None)
        self.laser = session.laser
        self.daq = session.daq
        self.sesion = session

        QtCore.QObject.connect(self.laser_widget.start_button, QtCore.SIGNAL('clicked()'), self.start_monitor)

        QtCore.QObject.connect(self.laser_widget.apply_button, QtCore.SIGNAL('clicked()'), self.update_laser)

    def update_laser(self):
        self.laser.wavelength = Q_(self.laser_widget.wavelength_line.text())
        print(Q_(self.laser_widget.start_wavelength_line.text()))
        self.laser.start_wavelength = Q_(self.laser_widget.start_wavelength_line.text())
        print(self.laser.start_wavelength)
        self.laser.stop_wavelength = Q_(self.laser_widget.stop_wavelength_line.text())
        print(Q_(self.laser_widget.stop_wavelength_line.text()))
        print(self.laser.stop_wavelength)
        self.laser.speed = Q_(self.laser_widget.speed_line.text())
        self.laser.trigger_step = Q_(self.laser_widget.trigger_step_line.text())
        self.laser.step = Q_(self.laser_widget.step_line.text())
        self.laser.power = Q_(self.laser_widget.power_line.text())
        self.laser.steps = int(self.laser_widget.steps_line.text())
        self.laser.wait = Q_(self.laser_widget.wait_line.text())
        self.laser.step_time = Q_(self.laser_widget.step_time_line.text())
        self.laser.sweeps = Q_(self.laser_widget.sweeps_line.text())

    def start_monitor(self):
        self.update_laser()
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
        for dev in self.devs_to_monitor:
            w = self.monitor[dev.properties['name']]
            w.main_plot.setLabel('bottom', 'Wavelength', units='nm')
            w.main_plot.showGrid(True, True)


        points = int(self.laser_widget.steps_line.text())
        conditions = {'devices': self.devs_to_monitor,
                      'accuracy': Q_('1 ms'),
                      'trigger': 'external',
                      'trigger_source': 'PFI0',
                      'points': points}
        task = self.daq.analog_input_setup(conditions)
        self.daq.trigger_analog(task)
        self.laser.steps = 1500
        self.laser.wavelength_sweeps = 4
        self.laser.disable_trigger()
        self.laser.lo()
        self.laser.step_time = Q_('1s')
        self.laser.execute_sweep()
        self.laser.software_trigger()
        while not self.laser.sweep_condition == 'Stop':
            sleep(0.5)

        conditions['points'] = 0
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