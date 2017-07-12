import os
from PyQt4 import QtCore, QtGui, uic
from .signal_monitor import SignalMonitorWidget

class MonitorConfig(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/monitor_config.ui'), self)
        self.ticks = []
        self.devices = []
        self.all_checked = False

        QtCore.QObject.connect(self.select_all, QtCore.SIGNAL('clicked()'), self.check_all )

    def populate_devices(self, devices):
        self.devices = devices
        for dev in devices:
            self.ticks.append(QtGui.QCheckBox())
            device_name = dev.properties['name']
            device_description = dev.properties['description']
            label = QtGui.QLabel(device_name)
            label.setToolTip(device_description)
            self.layout_widgets.addRow(label, self.ticks[-1])

    def check_all(self):
        if self.all_checked:
            for t in self.ticks:
                t.setChecked(False)
            self.all_checked = False
        else:
            for t in self.ticks:
                t.setChecked(True)
            self.all_checked = True



if __name__ == '__main__':
    import sys
    class test_device:
        def __init__(self):
            self.properties = {}
    dev1 = test_device()
    dev2 = test_device()
    dev1.properties = {'name': 'Photodiode 1',
            'description': 'Forward Intensity'}
    dev2.properties = {'name': 'Photodiode 2',
            'description': 'Backward Intensity'}

    devs = [dev1, dev2]
    app = QtGui.QApplication(sys.argv)
    window = MonitorConfig()
    window.populate_devices(devs)
    window.show()
    sys.exit(app.exec_())