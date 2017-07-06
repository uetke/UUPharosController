import sys

from pyqtgraph.Qt import QtGui, QtCore
from .laser_widget import LaserWidget

class MainWindowGUI(QtGui.QMainWindow):
    """ Monitor of the relevant signals.
    """
    def __init__(self,parent=None):
        QtGui.QMainWindow.__init__(self, parent=parent)
        self.setWindowTitle('Pharos Monitoring Software')

        self.central_widget = QtGui.QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QtGui.QHBoxLayout()

        self.comboBox = QtGui.QComboBox(self)

        dev = [{'name': 'test1'}, {'name': 'test2'}]
        self.setup_dropdown(dev)

        self.laser_widget = LaserWidget()

        self.layout.addWidget(self.laser_widget)
        self.layout.addWidget(self.comboBox)
        self.central_widget.setLayout(self.layout)

    def setup_dropdown(self, devices):
        for dev in devices:
            self.comboBox.addItem(dev['name'])

    def update_wavelength(self, wl):
        self.wavelength_line.setText = "%s nm" % wl

if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    mon = MainWindowGUI()
    mon.show()
    sys.exit(app.exec_())

