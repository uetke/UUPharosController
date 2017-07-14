from pyqtgraph.Qt import QtGui, QtCore
from .laser_widget import LaserWidget
from .monitor_config import MonitorConfig
from .signal_monitor import SignalMonitorWidget


class MainWindowGUI(QtGui.QMainWindow):
    """ Monitor of the relevant signals.
    """
    def __init__(self, laser, parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.setWindowTitle('Pharos Monitoring Software')

        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtGui.QHBoxLayout()

        self.laser_widget = LaserWidget(laser)

        self.layout.addWidget(self.laser_widget)

        self.central_widget.setLayout(self.layout)
        self.monitor_config_widget = MonitorConfig()
        QtCore.QObject.connect(self.laser_widget.start_button, QtCore.SIGNAL('clicked()'), self.apply_monitor)

        self.monitor = {}
        self.devs_to_monitor = []
        self.setup_actions()
        self.setup_menu()


    def apply_monitor(self):
        devs_to_monitor = []
        for i in range(len(self.monitor_config_widget.ticks)):
            if self.monitor_config_widget.ticks[i].isChecked():
                devs_to_monitor.append(self.monitor_config_widget.devices[i])

        for dev in devs_to_monitor:
            if dev.properties['name'] not in self.monitor:
                self.monitor[dev.properties['name']] = {'widget': SignalMonitorWidget()}
                self.monitor[dev.properties['name']]['widget'].set_name(dev.properties['description'])

            if not self.monitor[dev.properties['name']]['widget'].isVisible():
                self.monitor[dev.properties['name']]['widget'].show()
        self.devs_to_monitor = devs_to_monitor

    def update_wavelength(self, wl):
        self.wavelength_line.setText = "%s nm" % wl

    def setup_actions(self):
        self.monitor_config_action = QtGui.QAction("&Configure monitor", self)
        self.monitor_config_action.triggered.connect(self.monitor_config_widget.show)

    def setup_menu(self):
        self.menu = self.menuBar()
        self.monitor_menu = self.menu.addMenu("&Monitor")
        self.monitor_menu.addAction(self.monitor_config_action)




if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    mon = MainWindowGUI()
    mon.show()
    sys.exit(app.exec_())

