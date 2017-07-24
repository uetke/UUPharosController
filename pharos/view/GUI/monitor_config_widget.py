import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_
from pharos.view.GUI.signal_monitor import SignalMonitorWidget


class MonitorConfigWidget(QtGui.QWidget):
    def __init__(self, daqs, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/monitor_config.ui'), self)
        self.ticks = []
        self.groupbox = []
        self.devices = []
        self.all_checked = False
        self.monitors = {}

        self.populate_devices(daqs)

        QtCore.QObject.connect(self.select_all, QtCore.SIGNAL('clicked()'), self.check_all)

    def populate_devices(self, daqs):
        for d in daqs:
            self.groupbox.append(QtGui.QGroupBox())
            self.groupbox[-1].setTitle(d)
            layout = QtGui.QFormLayout()
            for dev in daqs[d]['input']:
                self.ticks.append(QtGui.QCheckBox())
                device_name = dev.properties['name']
                device_description = dev.properties['description']
                label = QtGui.QLabel(device_name)
                label.setToolTip(device_description)
                layout.addRow(label, self.ticks[-1])
                self.devices.append(dev)
            self.groupbox[-1].setLayout(layout)
            self.layout_widgets.addRow(self.groupbox[-1])
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
            conditions['trigger'] = 'external'
            conditions['trigger_source'] = self.trigger_info.text()
        elif self.trigger.currentIndex() == 1:
            conditions['trigger'] = 'internal'
            conditions['accuracy'] = Q_(self.accuracy.text())
        else:
            raise Exception('That trigger mode is not supported.')

        self.emit(QtCore.SIGNAL('conditions_ready'), conditions)




if __name__ == '__main__':
    import sys
    from pharos.model.experiment.measurement import measurement
    from pharos.model.lib.general_functions import from_yaml_to_dict

    config_experiment = "../../config/measurement.yml"
    experiment_dict = from_yaml_to_dict(config_experiment)
    experiment = measurement(experiment_dict)
    experiment.load_devices()
    experiment.initialize_devices()
    experiment.connect_all_devices_to_daq()
    experiment.connect_monitor_devices_to_daq()

    app = QtGui.QApplication(sys.argv)
    window = MonitorConfigWidget(experiment.daqs)
    window.show()
    sys.exit(app.exec_())