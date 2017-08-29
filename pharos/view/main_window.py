import numpy as np
import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_

from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI
from pharos.view.GUI.scan_config_widget import ScanConfigWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget
from pharos.view.GUI.wavelength_scan_widget import LaserScanWidget
from pharos.view.generic_work_thread import WorkThread

from pharos.config import config
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
        self.scan_timer = QtCore.QTimer()
        self.laser_timer = QtCore.QTimer()
        self.laser_timer.start(config.laser_update)

        # Load Widgets
        self.laser_widget = LaserWidgetGUI()
        self.monitor_widget = MonitorConfigWidget()
        self.scan_widget = ScanConfigWidget()
        self.laser_scan_widget = LaserScanWidget()
        self.laser_scan_widget.LaserWidgetDock.setWidget(self.laser_widget)
        self.laser_scan_widget.MonitorWidgetDock.setWidget(self.monitor_widget)
        self.laser_scan_widget.ScanWidgetDock.setWidget(self.scan_widget)

        # Make connections
        QtCore.QObject.connect(self.wavelength_scan_button, QtCore.SIGNAL('clicked()'), self.laser_scan_widget.show)

        QtCore.QObject.connect(self.wavelength_inc_button, QtCore.SIGNAL('clicked()'), self.increase_wavelength)
        QtCore.QObject.connect(self.wavelength_dec_button, QtCore.SIGNAL('clicked()'), self.decrease_wavelength)
        QtCore.QObject.connect(self.power_inc_button, QtCore.SIGNAL('clicked()'), self.increase_power)
        QtCore.QObject.connect(self.power_dec_button, QtCore.SIGNAL('clicked()'), self.decrease_power)

        QtCore.QObject.connect(self.wavelength_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_wavelength)
        QtCore.QObject.connect(self.power_slider, QtCore.SIGNAL('valueChanged(int)'), self.update_power)
        QtCore.QObject.connect(self.shutter, QtCore.SIGNAL('stateChanged(int)'), self.update_shutter)
        QtCore.QObject.connect(self.LD_current, QtCore.SIGNAL('stateChanged(int)'), self.update_ld_current)
        QtCore.QObject.connect(self.auto_power, QtCore.SIGNAL('stateChanged(int)'), self.update_auto_power)
        QtCore.QObject.connect(self.coherent_control, QtCore.SIGNAL('stateChanged(int)'), self.update_coherent_control)
        QtCore.QObject.connect(self.monitor_timer, QtCore.SIGNAL('timeout()'), self.update_monitors)
        QtCore.QObject.connect(self.scan_timer, QtCore.SIGNAL('timeout()'), self.update_scans)

        QtCore.QObject.connect(self.laser_scan_widget.start_button, QtCore.SIGNAL('clicked()'), self.start_monitor)
        QtCore.QObject.connect(self.laser_scan_widget.stop_button, QtCore.SIGNAL('clicked()'), self.stop_monitor)
        QtCore.QObject.connect(self.laser_scan_widget.pause_button, QtCore.SIGNAL('clicked()'), self.pause_monitor)
        QtCore.QObject.connect(self.laser_scan_widget.start_scan_button, QtCore.SIGNAL('clicked()'), self.start_scan)
        QtCore.QObject.connect(self.laser_scan_widget.stop_scan_button, QtCore.SIGNAL('clicked()'), self.stop_scan)
        QtCore.QObject.connect(self.laser_scan_widget.pause_scan_button, QtCore.SIGNAL('clicked()'), self.pause_scan)

        self.laser_widget.applyButton.clicked.connect(self.update_laser)
        self.laser_widget.readCurrent.clicked.connect(self.update_laser_widget)
        self.laser_timer.timeout.connect(self.update_values_from_laser)

        self.shutter_value = False
        self.monitor_paused = False
        self.monitor_running = False
        self.scan_running = False
        self.daq_enabled = False

        if self.laser.driver.sweep_condition != 'Stop':
            self.laser.driver.stop_sweep()

        self.laser_widget.populate_values(self.experiment.monitor['laser']['params'])
        self.scan_widget.populate_devices(self.experiment.daqs)
        self.monitor_widget.populate_devices(self.experiment.daqs)

    def update_laser(self):
        wavelength = Q_(self.laser_widget.wavelength.text())
        power = Q_(self.laser_widget.power.text())
        values = {
            'wavelength': wavelength,
            'powermW': power,
        }
        self.laser.driver.update(values)

    def update_wavelength(self, value):
        new_value = 1480+value*0.0001
        new_value = new_value*Q_('nm')
        self.wavelength.setText('{:4.4f~}'.format(new_value))
        self.laser.driver.wavelength = new_value

    def increase_wavelength(self):
        increase = Q_(self.wavelength_increment.text())
        self.laser.driver.wavelength = self.laser.driver.wavelength + increase

    def decrease_wavelength(self):
        increase = Q_(self.wavelength_increment.text())
        self.laser.driver.wavelength-=increase

    def increase_power(self):
        increase = Q_(self.power_increment.text())
        self.laser.driver.powermW += increase

    def decrease_power(self):
        increase = Q_(self.power_increment.text())
        self.laser.driver.powermW -= increase

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
        if self.monitor_running or self.monitor_paused or self.scan_running:
            raise Warning('Finish ongoing processes before triggering a new one.')

        devs_to_monitor = self.monitor_widget.get_devices_checked()
        if len(devs_to_monitor) > 0:
            self.monitor_widget.open_monitor(devs_to_monitor)
            self.experiment.monitor['detectors'] = devs_to_monitor
            self.experiment.monitor['laser']['params'] = self.laser_widget.update_laser_values()
            self.experiment.setup_continuous_scans()
            self.experiment.start_continuous_scans()
            time_to_scan = self.experiment.measure['monitor']['approx_time_to_scan'].m_as(Q_('ms'))
            start_wl = self.experiment.monitor['laser']['params']['start_wavelength']
            units = start_wl.u
            # Convert everything to the units of the start_wl
            start_wl = start_wl.m
            stop_wl = self.experiment.monitor['laser']['params']['stop_wavelength'].m_as(units)
            step = self.experiment.monitor['laser']['params']['interval_trigger'].m_as(units)
            num_points = (stop_wl - start_wl) / step+1
            xdata = np.linspace(start_wl, stop_wl, num_points)
            
            if self.experiment.monitor['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                self.monitor_widget.set_two_way_monitors(True)
            self.monitor_widget.set_wavelength_to_monitor(xdata)
            self.monitor_timer.start(time_to_scan/config.monitor_read_scan)
            self.daq_enabled = True
        else:
            self.daq_enabled = False
            self.laser.driver.execute_sweep()
        self.monitor_running = True

    def update_values_from_laser(self):
        wl = self.laser.driver.wavelength
        pw = self.laser.driver.powermW
        self.wavelength.setText('{:~}'.format(wl))
        self.power.setText('{:~}'.format(pw))
        condition = self.laser.driver.sweep_condition
        self.laser_status.setText(condition)
        if self.monitor_running and condition == 'Stop':
            self.stop_monitor()
        self.wavelength_slider.blockSignals(True)
        self.power_slider.blockSignals(True)
        self.wavelength_slider.setValue((wl.m_as('nm')-1480)/0.0001)
        self.power_slider.setValue((pw.m_as('mW')-0.01)/0.01)
        self.wavelength_slider.blockSignals(False)
        self.power_slider.blockSignals(False)
        self.LD_current.setChecked(self.laser.driver.LD_current)
        self.shutter.setChecked(self.laser.driver.shutter)
        self.auto_power.setChecked(self.laser.driver.auto_power)
        self.coherent_control.setChecked(self.laser.driver.coherent_control)

    def update_laser_widget(self):
        self.laser_widget.wavelength.setText('{:~}'.format(self.laser.driver.wavelength))
        self.laser_widget.power.setText('{:~}'.format(self.laser.driver.powermW))

    def start_scan(self):
        if self.monitor_running or self.monitor_paused or self.scan_running:
            print('Finish ongoing processes before triggering a new one.')
            return

        devs_to_monitor = self.monitor_widget.get_devices_checked()
        if len(devs_to_monitor) > 0:

            self.experiment.scan['detectors'] = devs_to_monitor
            self.experiment.scan['laser']['params'] = self.laser_widget.update_laser_values()
            self.experiment.scan['axis']['device'] = self.scan_widget.get_devices_and_values()
            self.experiment.setup_scan()

            start_wl = self.experiment.scan['laser']['params']['start_wavelength']
            stop_wl = self.experiment.scan['laser']['params']['stop_wavelength']
            step = self.experiment.scan['laser']['params']['interval_trigger']

            start_dev = self.experiment.scan['axis']['device']['range'][0]
            stop_dev = self.experiment.scan['axis']['device']['range'][1]
            step_dev = self.experiment.scan['axis']['device']['range'][2]

            axis = {'wavelength':
                        {'start': start_wl,
                         'stop': stop_wl,
                         'step': step},
                    'y_axis':
                        {'start': start_dev,
                         'stop': stop_dev,
                         'step': step_dev,
                         'name': self.experiment.scan['axis']['device']['name']}}

            self.scan_widget.configure_monitors(devs_to_monitor)
            self.scan_widget.open_monitor(devs_to_monitor)
            self.scan_widget.set_axis_to_monitor(axis)
            if self.experiment.scan['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                self.scan_widget.set_two_way_monitors(True)

            self.worker_thread = WorkThread(self.experiment.do_scan)
            self.worker_thread.start()
            time_to_scan = self.experiment.measure['scan']['approx_time_to_scan'].m_as(Q_('ms'))
            self.scan_timer.start(time_to_scan/config.monitor_read_scan)
            self.scan_running = True

    def stop_scan(self):
        if self.scan_running:
            self.scan_timer.stop()
            self.experiment.stop_scan()
            self.worker_thread.terminate()
            self.scan_running = False

    def pause_scan(self):
        """ Not yet implemented, it just stops the scan."""
        self.stop_scan()

    def update_scans(self):
        data = self.experiment.read_continuous_scans()
        self.scan_widget.update_signal_values(data)

    def update_monitors(self):
        if self.daq_enabled:
            data = self.experiment.read_continuous_scans()
            self.monitor_widget.update_signal_values(data)
        
    def stop_monitor(self):
        if not (self.monitor_running or self.monitor_paused):
            return

        if self.daq_enabled:
            self.monitor_timer.stop()
            self.update_monitors()
            self.experiment.stop_continuous_scans()
        else:
            self.experiment.stop_laser()
        self.daq_enabled = False
        self.monitor_paused = False
        self.monitor_running = False

    def pause_monitor(self):
        if self.monitor_paused:
            self.experiment.resume_continuous_scans()
            self.monitor_paused = False
            self.monitor_running = True 
            return
        self.monitor_timer.stop()
        self.experiment.pause_continuous_scans()
        self.monitor_paused = True
        self.monitor_running = False

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            if self.monitor_running:
                self.stop_monitor()
            self.monitor_widget.close_all_monitors()
            self.laser_widget.close()
            self.laser_widget.deleteLater()
            self.monitor_widget.close()
            self.monitor_widget.deleteLater()
            self.scan_widget.close()
            self.laser_scan_widget.close()
            self.laser_scan_widget.deleteLater()
            self.monitor_widget.deleteLater()
            self.laser.driver.finalize()
            event.accept()
        else:
            event.ignore()