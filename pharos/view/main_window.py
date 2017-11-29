"""
    main_window
    ===========
    Holds the GUI logic. It is responsible for bindin buttons, processing signals, etc.
    Doesn't deal with layout concerns, those are located in the GUI folder.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
import numpy as np
import os
import time
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_

from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI
from pharos.view.GUI.scan_config_widget import ScanConfigWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget
from pharos.view.GUI.wavelength_scan_widget import LaserScanWidget
from pharos.view.GUI.rotation_stage_gui import ThorlabsRotationWidgetGUI
from pharos.view.GUI.shutter_gui import ShutterGui
from pharos.view.generic_work_thread import WorkThread

from pharos.config import config
import pharos.view.GUI.QtCreator.resources_rc


class MainWindow(QtGui.QMainWindow):
    def __init__(self, experiment, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/QtCreator/main_window.ui'), self)
        self.experiment = experiment
        self.experiment.line_finished.connect(self.update_monitors)

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

        self.laser_scan_widget.start_button.clicked.connect(self.start_monitor)
        self.laser_scan_widget.stop_button.clicked.connect(self.stop_monitor)
        self.laser_scan_widget.pause_button.clicked.connect(self.pause_monitor)
        self.laser_scan_widget.start_scan_button.clicked.connect(self.start_scan)
        self.laser_scan_widget.stop_scan_button.clicked.connect(self.stop_scan)
        self.laser_scan_widget.pause_scan_button.clicked.connect(self.pause_scan)
        self.laser_scan_widget.save_all_button.clicked.connect(self.save_all_monitors)
        self.laser_widget.applyButton.clicked.connect(self.update_laser)
        self.laser_widget.readCurrent.clicked.connect(self.update_laser_widget)
        self.laser_timer.timeout.connect(self.update_values_from_laser)

        self.shutter_value = False
        self.monitor_paused = False
        self.monitor_running = False
        self.scan_running = False
        self.daq_enabled = False
        self.directory = None
        self.curr_sweep = 0

        if 'default_directory' in self.experiment.init:
            self.directory = self.experiment.init['default_directory']
        
        if self.laser.driver.sweep_condition != 'Stop':
            self.laser.driver.stop_sweep()

        self.laser_widget.populate_values(self.experiment.monitor['laser']['params'])
        self.scan_widget.populate_devices(self.experiment)
        self.monitor_widget.populate_data(self.experiment)

        if len(self.experiment.rotation_stages) > 0:
            self.rotation_stages_widget = []
            self.rotation_actions = []
            for rot in self.experiment.rotation_stages:
                dev = self.experiment.devices[rot]
                self.rotation_stages_widget.append(ThorlabsRotationWidgetGUI(dev))
                self.rotation_actions.append(QtGui.QAction(dev.properties['name'], self))
                self.rotation_actions[-1].triggered.connect(self.rotation_stages_widget[-1].show)
                self.menuDevices.addAction(self.rotation_actions[-1])

        if 'shutter' in self.experiment.scan:
            self.shutter_widget = ShutterGui(self.experiment)
            self.shutter_action = QtGui.QAction('Shutter Control', self)
            self.shutter_action.triggered.connect(self.shutter_widget.show)
            self.menuDevices.addAction(self.shutter_action)

    def update_laser(self):
        """
        Gets the values from the laser_widget and sends them to the laser. It only deals with the wavelength and the
        power. The rest of the values are passed to the scan and are therefore not for modifying the laser in-vivo.
        """
        wavelength = Q_(self.laser_widget.wavelength.text())
        power = Q_(self.laser_widget.power.text())
        values = {
            'wavelength': wavelength,
            'powermW': power,
        }
        self.laser.driver.update(values)

    def update_wavelength(self, value):
        """
        Updates the wavelength text and laser. It is triggered from the sliding bar.

        .. todo:: The value is in the range (0, something) and is converted to wavelength assuming the lower limit of
        the laser is 1480, which is true for the Santec, but not universal. The should be a way of retrieving the lower
        limit at runtime.

        """
        new_value = 1480+value*0.0001
        new_value = new_value*Q_('nm')
        self.wavelength.setText('{:4.4f~}'.format(new_value))
        self.laser.driver.wavelength = new_value

    def increase_wavelength(self):
        """Increases the wavelength by the amount specified in the GUI. """
        increase = Q_(self.wavelength_increment.text())
        self.laser.driver.wavelength = self.laser.driver.wavelength + increase

    def decrease_wavelength(self):
        """Decreases the wavelength by the amount specified in the GUI"""
        increase = Q_(self.wavelength_increment.text())
        self.laser.driver.wavelength-=increase

    def increase_power(self):
        """Increases the power by the amount specified in the GUI."""
        increase = Q_(self.power_increment.text())
        self.laser.driver.powermW += increase

    def decrease_power(self):
        """ Decreases the power by the amount specified in the GUI. """
        increase = Q_(self.power_increment.text())
        self.laser.driver.powermW -= increase

    def update_shutter(self, state):
        """ Updates the status of the shutter. If it was open, changes to close and the opposite. """
        state = bool(state)
        self.laser.driver.shutter = state

    def update_ld_current(self, state):
        """ Updates the status of the LD_current."""
        state = bool(state)
        self.laser.driver.LD_current = state

    def update_auto_power(self, state):
        state = bool(state)
        self.laser.driver.auto_power = state

    def update_coherent_control(self, state):
        """ Updates the cohernt control status. """
        state = bool(state)
        self.laser.driver.coherent_control = state

    def update_power(self, value):
        """ Updates the power of the laser. It is triggered when the sliding bar changes position. """
        new_value = 0.01+value*0.01
        new_value = new_value*Q_('mW')
        self.power.setText('{:1.2f~}'.format(new_value))
        self.laser.driver.powermW = new_value

    def start_monitor(self):
        """ Starts the monitor of one or several signals.
        It reads the parameters from the GUI and loads them into the experiment class.
        If there are detectors selected, it opens the window to display the data; if nothing is selected, it just
        triggers the laser and does not start the NI-card for acquiring.
        """
        if self.monitor_running or self.monitor_paused or self.scan_running:
            if self.monitor_widget.wait_for_each_line.isChecked():
                self.experiment.wait_for_line = True
                self.curr_sweep = 0  # Current number of wavelength sweep
                self.worker_monitor_thread = WorkThread(self.experiment.continuous_scans_waiting)
                self.worker_monitor_thread.start()
            else:
                self.laser.driver.execute_sweep()
                print('Triggering the laser again.')
                laser = self.experiment.devices[self.experiment.monitor['laser']['name']]
                laser.apply_values(self.experiment.monitor['laser']['params'])
            return
        
        devs_to_monitor = self.monitor_widget.get_devices_checked()
        if len(devs_to_monitor) > 0:
            self.monitor_widget.open_monitor(devs_to_monitor)
            self.experiment.monitor['detectors'] = devs_to_monitor
            self.experiment.monitor['laser']['params'] = self.laser_widget.update_laser_values()

            if self.monitor_widget.trigger.currentText() == 'External':
                self.experiment.monitor['daq']['trigger'] = 'external'
            elif self.monitor_widget.trigger.currentText() == 'Internal':
                self.experiment.monitor['daq']['trigger'] = 'internal'
            else:
                print('Something is wrong with the dropdown choices')
            if self.monitor_widget.trigger_adc.text() != '':
                self.experiment.monitor['daq']['trigger_source'] = self.monitor_widget.trigger_adc.text()
            else:
                self.experiment.monitor['daq']['trigger_source'] = None
            if self.monitor_widget.trigger_start.text() != '':
                self.experiment.monitor['daq']['start_source'] = self.monitor_widget.trigger_start.text()
            else:
                self.experiment.monitor['daq']['start_source'] = None

            #  Set the number of accumulations to the monitor, first do this, then set the wavelength.
            accumulations = self.laser_scan_widget.accumulations_line.text()
            if accumulations is not None or accumulations != '' :
                try:
                    accumulations = int(accumulations)
                except:
                    accumulations = 1       
                if not accumulations > 0:
                    accumulations = 1
            else:
                self.laser_scan_widget.accumulations_line.setText('1')
                accumulations = 1
            self.monitor_widget.set_accumulations_to_monitor(accumulations)

            self.experiment.setup_continuous_scans()

            start_wl = self.experiment.monitor['laser']['params']['start_wavelength']
            units = start_wl.u
            # Convert everything to the units of the start_wl
            start_wl = start_wl.m
            stop_wl = self.experiment.monitor['laser']['params']['stop_wavelength'].m_as(units)
            step = self.experiment.monitor['laser']['params']['interval_trigger'].m_as(units)
            num_points = round((stop_wl - start_wl) / step)+1
            xdata = np.linspace(start_wl, stop_wl, num_points)
            if self.experiment.monitor['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                self.monitor_widget.set_two_way_monitors(True)
            self.monitor_widget.set_wavelength_to_monitor(xdata)
            if self.monitor_widget.wait_for_each_line.isChecked():
                self.experiment.wait_for_line = True
                self.curr_sweep = 0  # Current number of wavelength sweep
                self.worker_monitor_thread = WorkThread(self.experiment.continuous_scans_waiting)
                self.worker_monitor_thread.start()
            else:
                self.worker_monitor_thread = None
                self.experiment.wait_for_line = False
                self.experiment.start_continuous_scans()
                self.monitor_timer.start(config.monitor_read_scan)

            self.laser_condition = 'Running'
            self.daq_enabled = True
        else:
            self.daq_enabled = False
            self.laser.driver.execute_sweep()
        self.monitor_running = True

    def update_values_from_laser(self):
        """ Reads the values from the laser and passes them to the GUI. It also blocks the signals of the sliders to
        avoid an infinite loop: update the slide=>update the value=>update the slide, etc.
        If the laser would be able to check the status of the LD_current, Shutter, etc, it would update it on the GUI.
        A driver built on top of the IEEE standar is able to do it, and I have already included the first steps in the
        controllers folder.

        """
        wl = self.laser.driver.wavelength
        pw = self.laser.driver.powermW
        self.wavelength.setText('{:~}'.format(wl))
        self.power.setText('{:~}'.format(pw))
        condition = self.laser.driver.sweep_condition
        self.laser_condition = condition
        self.laser_status.setText(condition)
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
        """ Updates the values displayed in the GUI. It is triggerend only on demand from the user. """
        self.laser_widget.wavelength.setText('{:~}'.format(self.laser.driver.wavelength))
        self.laser_widget.power.setText('{:~}'.format(self.laser.driver.powermW))

    def start_scan(self):
        if self.monitor_running or self.monitor_paused or self.scan_running:
            self.stop_monitor()
            raise Warning('Finishing ongoing processes before triggering a new one.')
            return

        devs_to_monitor = self.monitor_widget.get_devices_checked()
        if len(devs_to_monitor) > 0:

            self.experiment.scan['detectors'] = devs_to_monitor
            # Read the delay from the GUI
            delay = self.scan_widget.delay.text()
            if delay != "":
                delay = Q_(delay)
                self.experiment.scan['shutter']['delay'] = delay

            self.experiment.scan['laser']['params'] = self.laser_widget.update_laser_values()
            values = self.scan_widget.get_devices_and_values()
            self.experiment.scan['axis']['device']['name'] = values['name']
            self.experiment.scan['axis']['device']['property'] = values['output']
            self.experiment.scan['axis']['device']['range'] = values['range']
            if self.monitor_widget.trigger.currentText() == 'External':
                self.experiment.scan['daq']['trigger'] = 'external'
            elif self.monitor_widget.trigger.currentText() == 'Internal':
                self.experiment.scan['daq']['trigger'] = 'internal'
            else:
                print('There is something wrong with the dropdown choices')

            if self.monitor_widget.trigger_adc.text() != '':
                self.experiment.scan['daq']['trigger_source'] = self.monitor_widget.trigger_adc.text()
            else:
                self.experiment.scan['daq']['trigger_source'] = None
            if self.monitor_widget.trigger_start.text() != '':
                self.experiment.scan['daq']['start_source'] = self.monitor_widget.trigger_start.text()
            else:
                self.experiment.scan['daq']['start_source'] = None

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
            if self.experiment.scan['laser']['params']['sweep_mode'] in ('ContTwo', 'StepTwo'):
                self.scan_widget.set_two_way_monitors(True)
                if self.scan_widget.average_plot.isChecked():
                    self.scan_widget.set_average_monitors(True)
                elif self.scan_widget.difference_plot.isChecked():
                    self.scan_widget.set_difference_monitors(True)

            self.scan_widget.set_axis_to_monitor(axis)
            self.worker_thread = WorkThread(self.experiment.do_scan)
            self.worker_thread.start()
            time_to_scan = self.experiment.measure['scan']['approx_time_to_scan'].m_as(Q_('ms'))
            if self.monitor_widget.wait_for_each_line.isChecked():
                self.experiment.wait_for_line = True
                self.experiment.line_scan_finished.connect(self.update_scans)
            else:
                self.scan_timer.start(config.monitor_read_scan)
            self.scan_running = True
            self.t0 = time.time()

    def stop_scan(self):
        if self.scan_running:
            self.scan_timer.stop()
            self.experiment.stop_scan()
            self.worker_thread.terminate()
            self.scan_running = False

    def pause_scan(self):
        """ Not yet implemented, it just stops the scan."""
        self.stop_scan()
            
    def update_scans(self, data=None):
        if data is None:
            data = self.experiment.read_continuous_scans()
        self.scan_widget.update_signal_values(data)

    def update_monitors(self, data=None):
        if self.daq_enabled:
            if data is None:
                data = self.experiment.read_continuous_scans()
            new_data = 0
            for d in data:
                new_data += len(data[d])
            if new_data > 0:
                self.monitor_widget.update_signal_values(data)               
        
    def stop_monitor(self):
        if not (self.monitor_running or self.monitor_paused):
            return

        if self.daq_enabled:
            print('Stopping cont scans')
            if self.worker_monitor_thread is not None:
                print('Terminating worker thread')
                self.worker_monitor_thread.terminate()
            else:
                self.monitor_timer.stop()
                #self.update_monitors()
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
        #self.monitor_timer.stop()
        self.experiment.pause_continuous_scans()
        self.monitor_paused = True
        self.monitor_running = False

    def save_all_monitors(self):
        if self.directory is None:
            self.choose_dir()
        else:
            self.monitor_widget.save_all_monitors(self.directory)

    def choose_dir(self):
        if self.directory is None:
            if os.path.exists("D:/Data"):
                self.directory = "D:/Data"
            elif os.path.exists("~"):
                self.directory = "~"

        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        self.save()

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