import numpy as np
import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_

from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI
from pharos.view.GUI.scan_config_widget import ScanConfigWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget
import pharos.view.GUI.QtCreator.resources_rc

class MainWindow(QtGui.QMainWindow):
    def __init__(self, experiment, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/QtCreator/main_window.ui'), self)
        self.experiment = experiment
        self.laser = self.experiment.devices[experiment.measure['scan']['laser']['name']]
        self.daqs = self.experiment.daqs

        self.monitor_timer = QtCore.QTimer()

        # Load Widgets
        self.laser_widget = LaserWidgetGUI(parent = self)
        self.monitor_widget = MonitorConfigWidget()
        self.scan_widget = ScanConfigWidget()

        # Make connections
        QtCore.QObject.connect(self.apply_laser, QtCore.SIGNAL('clicked()'), self.update_laser)
        QtCore.QObject.connect(self.laser_button, QtCore.SIGNAL('clicked()'), self.laser_widget.show)
        QtCore.QObject.connect(self.monitor_button, QtCore.SIGNAL('clicked()'), self.monitor_widget.show)
        QtCore.QObject.connect(self.close_monitors_button, QtCore.SIGNAL('clicked()'), self.monitor_widget.close_all_monitors)
        QtCore.QObject.connect(self.wavelength_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_wavelength)
        QtCore.QObject.connect(self.power_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_power)
        QtCore.QObject.connect(self.shutter, QtCore.SIGNAL('stateChanged(int)'), self.update_shutter)
        QtCore.QObject.connect(self.LD_current, QtCore.SIGNAL('stateChanged(int)'), self.update_ld_current)
        QtCore.QObject.connect(self.auto_power, QtCore.SIGNAL('stateChanged(int)'), self.update_auto_power)
        QtCore.QObject.connect(self.coherent_control, QtCore.SIGNAL('stateChanged(int)'), self.update_coherent_control)
        QtCore.QObject.connect(self.monitor_timer, QtCore.SIGNAL('timeout()'), self.update_monitors)
        QtCore.QObject.connect(self.start_button, QtCore.SIGNAL('clicked()'), self.start_monitor)
        QtCore.QObject.connect(self.stop_button, QtCore.SIGNAL('clicked()'), self.stop_monitor)
        QtCore.QObject.connect(self.pause_button, QtCore.SIGNAL('clicked()'), self.pause_monitor)
        QtCore.QObject.connect(self.scan_button, QtCore.SIGNAL('clicked()'), self.scan_widget.show)

        self.wavelength.setText('{:~}'.format(self.laser.driver.wavelength))
        self.power.setText('{:~}'.format(self.laser.driver.powermW))
        self.wavelength_slider.setValue((self.laser.driver.wavelength.m_as('nm')-1480)/0.0001)
        self.power_slider.setValue((self.laser.driver.powermW.m_as('mW')-0.01)/0.01)
        self.shutter_value = False
        self.monitor_paused = False
        self.monitor_running = False
        self.scan_running = False

        self.laser_widget.populate_values(self.experiment.monitor['laser']['params'])
        self.scan_widget.populate_daq_devices(self.experiment.daqs)
        self.monitor_widget.populate_devices(self.experiment.daqs)

    def update_laser(self):
        wavelength = Q_(self.wavelength.text())
        power = Q_(self.power.text())
        values = {
            'wavelength': wavelength,
            'powermW': power,
        }
        self.wavelength_slider.setValue((wavelength.m_as(Q_('nm')) - 1480) / 0.0001)
        self.laser.driver.update(values)

    def update_wavelength(self, value):
        new_value = 1480+value*0.0001
        new_value = new_value*Q_('nm')
        self.wavelength.setText('{:4.4f~}'.format(new_value))
        self.laser.driver.wavelength = new_value

    def update_shutter(self, state):
        state = bool(state)
        self.laser.driver.shutter = state

    def update_ld_current(self, state):
        state = bool(state)
        self.laser.driver.LD_current = state

    def update_auto_power(self, state):
        state = bool(state)
        self.laser.driver.auto_power = state

    def update_coherent_control(self, state):
        state = bool(state)
        self.laser.driver.coherent_control = state

    def update_power(self, value):
        new_value = 0.01+value*0.01
        new_value = new_value*Q_('mW')
        self.power.setText('{:1.2f~}'.format(new_value))
        self.laser.driver.powermW = new_value

    def start_monitor(self):
        if self.monitor_paused:
            self.experiment.resume_continuous_scans()
            self.start_button.setText('Pause')
            self.monitor_paused = False
            self.monitor_running = True
            return

        devs_to_monitor = self.monitor_widget.get_devices_checked()
        self.monitor_widget.open_monitor(devs_to_monitor)
        if len(devs_to_monitor) > 0:
            self.experiment.monitor['detectors'] = devs_to_monitor
            self.experiment.monitor['laser']['params'] = self.laser_widget.update_laser_values()
            self.experiment.setup_continuous_scans()
            self.experiment.start_continuous_scans()
            time_to_scan = self.experiment.measure['monitor']['approx_time_to_scan'].m_as(Q_('s'))
            start_wl = self.experiment.monitor['laser']['params']['start_wavelength']
            units = start_wl.u
            # Convert everything to the units of the start_wl
            start_wl = start_wl.m
            stop_wl = self.experiment.monitor['laser']['params']['stop_wavelength'].m_as(units)
            step = self.experiment.monitor['laser']['params']['trigger_step'].m_as(units)
            num_points = (stop_wl - start_wl) / step
            xdata = np.linspace(start_wl, stop_wl, num_points)
            
            if self.experiment.monitor['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                self.monitor_widget.set_two_way_monitors(True)
            self.monitor_widget.set_wavelength_to_monitor(xdata)
            self.monitor_timer.start(time_to_scan/10)
        else:
            self.laser.driver.execute_sweep()
        self.start_button.setText('Pause')
        self.monitor_running = True

    def update_monitors(self):
        data = self.experiment.read_continuous_scans()
        self.wavelength.setText('{:~}'.format(self.laser.driver.wavelength))
        self.laser_status.setText(self.laser.driver.sweep_condition)
        if self.laser.driver.sweep_condition == 'Stop':
            self.laser.driver.execute_sweep()

        self.monitor_widget.update_signal_values(data)
        
    def stop_monitor(self):
        self.start_button.setText('Start')
        self.monitor_timer.stop()
        self.update_monitors()
        self.experiment.stop_continuous_scans()
        self.wavelength.setText('{:~}'.format(self.laser.driver.wavelength))
        self.laser_status.setText(self.laser.driver.sweep_condition)
        self.monitor_paused = False
        self.monitor_running = False

    def pause_monitor(self):
        self.monitor_timer.stop()
        self.experiment.pause_continuous_scans()
        self.start_button.setText('Resume')
        self.monitor_paused = True
        self.monitor_running = False

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if self.monitor_running:
                self.stop_monitor()
            event.accept()
        else:
            event.ignore()