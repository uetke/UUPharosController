from pyqtgraph.Qt import QtGui, QtCore
from pharos.view.GUI.laser_widget import LaserWidget
from pharos.view.GUI.monitor_config_widget import MonitorConfigWidget


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
        self.monitor_config_widget = MonitorConfigWidget()
        self.layout.addWidget(self.laser_widget)
        self.layout.addWidget(self.monitor_config_widget)

        self.central_widget.setLayout(self.layout)

        self.setup_actions()
        self.setup_menu()

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
    class laser(object):
        pass

    app = QApplication(sys.argv)
    mon = MainWindowGUI(laser)
    mon.show()
    sys.exit(app.exec_())

