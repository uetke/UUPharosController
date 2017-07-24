import numpy as np
from PyQt4 import QtCore
from pharos.view.GUI.mainwindow_old import MainWindowGUI


class MainWindow(MainWindowGUI):
    def __init__(self, session):
        MainWindowGUI.__init__(self, session.laser, parent=None)
        self.laser = session.laser
        self.daq = session.daq
        self.session = session
        self.monitor_task = None

        self.monitor_timer = QtCore.QTimer()

        QtCore.QObject.connect(self.laser_widget.start_button, QtCore.SIGNAL('clicked()'), self.laser_widget.configure_laser)
        QtCore.QObject.connect(self.laser_widget, QtCore.SIGNAL('configure_monitor'), self.monitor_config_widget.apply_monitor)
        QtCore.QObject.connect(self.monitor_config_widget, QtCore.SIGNAL('conditions_ready'), self.start_monitor)
        QtCore.QObject.connect(self.monitor_timer, QtCore.SIGNAL("timeout()"), self.update_monitor)
        QtCore.QObject.connect(self.laser_widget.stop_button, QtCore.SIGNAL('clicked()'), self.stop)
        QtCore.QObject.connect(self.laser_widget.pause_button, QtCore.SIGNAL('clicked()'), self.pause)
        #QtCore.QObject.connect(self.laser_widget.apply_button, QtCore.SIGNAL('clicked()'), self.update_laser)

        self.monitor_config_widget.populate_devices(self.session.daq_devices)
        self.laser_widget.populate_values(self.session.laser_defaults)

    def start_monitor(self, conditions):
        if self.monitor_task is not None:
            if not self.daq.is_task_complete(self.monitor_task):
                print('Trying to trigger again the monitor')
                return False
        
        self.devices_monitored = conditions['devices']
        start_wl = self.laser.start_wavelength
        stop_wl = self.laser.stop_wavelength
        step = self.laser.trigger_step
        num_points = (stop_wl - start_wl) / step
        xdata = np.linspace(start_wl, stop_wl, num_points)
        
        for dev in self.devices_monitored:
            self.monitor_config_widget.monitors[dev.properties['name']]['widget'].set_wavelength(xdata)
        
        self.monitor_task = self.daq.analog_input_setup(conditions)
        self.daq.trigger_analog(self.monitor_task)
        self.laser.execute_sweep()
        self.laser_widget.current_condition_line.setText(self.laser.sweep_condition)
        self.monitor_timer.start(100) # In ms

    def update_monitor(self):
        self.laser_widget.wavelength_line.setText('{:~}'.format(self.laser.wavelength))
        conditions = {'points': -1}
        try:
            v, d = self.daq.read_analog(self.monitor_task, conditions)
        except:
            return
        num_devs = len(self.devices_monitored)
        data = d[:v*num_devs]
        data = np.reshape(data, (num_devs, int(len(data) / num_devs)))

        for i in range(num_devs):
            dev = self.devices_monitored[i]
            new_data = data[:,i]
            self.monitor_config_widget.monitors[dev.properties['name']]['widget'].set_ydata(new_data)
            self.monitor_config_widget.monitors[dev.properties['name']]['widget'].update_monitor()

        if self.daq.is_task_complete(self.monitor_task):
            self.monitor_task = None
            self.monitor_timer.stop()
        self.laser_widget.current_condition_line.setText(self.laser.sweep_condition)
        
    def stop(self):
        self.laser.stop_sweep()
        self.laser_widget.current_condition_line.setText(self.laser.sweep_condition)
        self.monitor_timer.stop()
        
    def pause(self):
        self.laser.pause_sweep()
        self.laser_widget.current_condition_line.setText(self.laser.sweep_condition)



if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    import sys
    from pharos.model.lib.session import session
    session.laser = None
    session.daq = None

    ap = QApplication(sys.argv)
    window = MainWindow(session)
    window.show()
    ap.exit(ap.exec_())