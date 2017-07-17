import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_
from .signal_monitor import SignalMonitorWidget


class MonitorConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/monitor_config.ui'), self)
        self.ticks = []
        self.devices = []
        self.all_checked = False
        self.monitors = {}

        QtCore.QObject.connect(self.select_all, QtCore.SIGNAL('clicked()'), self.check_all )

    def populate_devices(self, devices):
        self.devices = []
        for dev in devices:
            if dev.properties['mode'] == 'input':
                self.ticks.append(QtGui.QCheckBox())
                device_name = dev.properties['name']
                device_description = dev.properties['description']
                label = QtGui.QLabel(device_name)
                label.setToolTip(device_description)
                self.layout_widgets.addRow(label, self.ticks[-1])
                self.devices.append(dev)
        self.configure_monitors(self.devices)

    def check_all(self):
        if self.all_checked:
            for t in self.ticks:
                t.setChecked(False)
            self.all_checked = False
        else:
            for t in self.ticks:
                t.setChecked(True)
            self.all_checked = True

    def configure_monitors(self, devs_to_monitor):
        for dev in devs_to_monitor:
            if dev.properties['name'] not in self.monitors:
                self.monitors[dev.properties['name']] = {'widget': SignalMonitorWidget()}
                self.monitors[dev.properties['name']]['widget'].set_name(dev.properties['description'])

    def apply_monitor(self, conditions):
        conditions['devices'] = []
        for i in range(len(self.ticks)):
            if self.ticks[i].isChecked():
                conditions['devices'].append(self.devices[i])
                self.monitors[self.devices[i].properties['name']]['widget'].show()

        if self.trigger.currentIndex() == 0:
            self.conditions['trigger'] = 'external'
            self.conditions['trigger_source'] = self.trigger_info.text()
        elif self.trigger.currentIndex() == 1:
            self.conditions['trigger'] = 'internal'
            self.conditions['accuracy'] = Q_(self.accuracy.text())
        else:
            raise Exception('That trigger mode is not supported.')

        self.emit(QtCore.SIGNAL('conditions_ready'), conditions)




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
    window = MonitorConfigWidget()
    window.populate_devices(devs)
    window.show()
    sys.exit(app.exec_())