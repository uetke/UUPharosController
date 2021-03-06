"""
    scan_config_widget
    ==================
    Widget for configuring a 2D scan with a laser scanning wavelengths.
    It started with the idea of allowing N-D scans (by adding more than one device) but it proved not
    to be the best approach (start from simple and build to complicated).
    However the GUI allows to setup more than one device by clicking a + button (now disabled).

    :copyright: 2017
    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""

import os
from PyQt4 import QtGui, uic
from lantz import Q_
from pharos.view.GUI.scan_monitor import ScanMonitorWidget


class ScanConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/scan_config.ui'), self)

        self.devices_widget = []
        self.devices_input = []
        self.devices = []
        self.monitors = {}

        #self.add_device_button.clicked[bool].connect(self.add_new_device)
        #self.remove_device_button.clicked[bool].connect(self.remove_last_device)
        self.i = 0

    def populate_devices(self, experiment):
        """ Adds group boxes for all the output devices connected to the daqs and Time at the end.
        :param experiment: Experiment class."""

        for d in experiment.output_devices:
            self.devices = []
            for o in d.properties['outputs']:
                self.devices.append({'dev': d,
                                    'output': o})

                self.add_new_device(self.devices[-1])

    def configure_monitors(self, devs_to_monitor):
        for dev in devs_to_monitor:
            if dev.properties['name'] in self.monitors:
                self.monitors[dev.properties['name']]['widget'].clear_data()
                self.monitors[dev.properties['name']]['widget'].close()
                #self.monitors[dev.properties['name']]['widget'].deleteLater()

            self.monitors[dev.properties['name']] = {'widget': ScanMonitorWidget()}
            self.monitors[dev.properties['name']]['widget'].clear_data()
            self.monitors[dev.properties['name']]['widget'].set_name(dev.properties['description'])

    def open_monitor(self, devs):
        """Opens the signal monitor window for the given devices."""
        for dev in devs:
            self.monitors[dev.properties['name']]['widget'].show()
            #self.monitors[dev.properties['name']]['widget'].clear_data()

    def set_axis_to_monitor(self, axis):
        """Sets the axis information to the monitors."""
        for mon in self.monitors:
            self.monitors[mon]['widget'].set_axis(axis)

    def update_signal_values(self, data):
        """Updates the data to the different monitors."""
        for dev in data:
            self.monitors[dev]['widget'].set_data(data[dev])

    def set_two_way_monitors(self, two_way=True):
        for m in self.monitors:
            self.monitors[m]['widget'].two_way = two_way

    def set_average_monitors(self, average=True):
        for m in self.monitors:
            self.monitors[m]['widget'].average = average

    def set_difference_monitors(self, difference=True):
        for m in self.monitors:
            self.monitors[m]['widget'].difference = difference

    def close_all_monitors(self):
        for m in self.monitors:
            self.monitors[m]['widget'].close()
            self.monitors[m]['widget'].deleteLater()

    def add_new_device(self, dev):
        ind = len(self.devices_widget)
        name = "{} => {}".format(dev['dev'], dev['output'])
        self.devices_widget.append(DeviceScan(name=name, index=ind, parent=self))
        self.devices_layout.addWidget(self.devices_widget[-1])

    def remove_last_device(self):
        self.devices_layout.removeWidget(self.devices_widget[-1])
        self.devices_widget[-1].deleteLater()
        del self.devices_widget[-1]

    def get_devices_and_values(self):
        for dev in self.devices_widget:
            v = dev.get_values()
            if v['radio']:
                break

        dev = self.devices[v['index']]

        values= {
            'name': dev['dev'].properties['name'],
            'output': dev['output'],
            'range': v['range'],
        }
        
        return values


class DeviceScan(QtGui.QWidget):
    def __init__(self, name=None, index=0, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)

        self.layout = QtGui.QHBoxLayout()
        self.dev_name = QtGui.QLineEdit()
        if name is not None:
            self.dev_name.setText(name)
        self.min_line = QtGui.QLineEdit()
        self.max_line = QtGui.QLineEdit()
        self.step_line = QtGui.QLineEdit()
        self.radio = QtGui.QRadioButton()

        self.layout.addWidget(self.radio)
        self.layout.addWidget(self.dev_name)
        self.layout.addWidget(self.min_line)
        self.layout.addWidget(self.max_line)
        self.layout.addWidget(self.step_line)

        self.setLayout(self.layout)
        self.index = index


    def check_limits(self):
        red_background =  "QLineEdit { background: rgb(255, 20, 20); selection-background-color: rgb(233, 99, 0); }"
        white_background = "QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(233, 99, 0); }"
        dev = self.devices[self.dropdown.currentText()]
        if dev == 'time':
            self.min_line.setStyleSheet(white_background)
            self.max_line.setStyleSheet(white_background)
            return
        dev_min = Q_(dev.properties['limits']['min'])
        dev_max = Q_(dev.properties['limits']['max'])

        min_text = self.min_line.text()
        max_text = self.max_line.text()
        if min_text != "":
            min_value = Q_(min_text)
            if dev_min <= min_value <= dev_max:
                self.min_line.setStyleSheet(white_background)
            else:
                self.min_line.setStyleSheet(red_background)
        else:
            self.min_line.setStyleSheet(white_background)

        if max_text != "":
            max_value = Q_(max_text)
            if dev_min <= max_value <= dev_max:
                self.max_line.setStyleSheet(white_background)
            else:
                self.max_line.setStyleSheet(red_background)
        else:
            self.max_line.setStyleSheet(white_background)

    def get_values(self):
        min_value = Q_(self.min_line.text())
        max_value = Q_(self.max_line.text())
        step_value = Q_(self.step_line.text())

        values = {
            'index': self.index,
            'radio': self.radio.isChecked(),
            'range': [min_value, max_value, step_value, ]
        }
        return values



if __name__ == "__main__":
    import sys

    class dev:
        pass
    dev1 = dev()
    dev1.properties = {'name': "Name 1",
            "description": "Description 1",
                       'limits': {'min': '10nm',
                                  'max': '20nm'}
                       }
    dev2 = dev()
    dev2.properties = {'name': 'Name 2',
                       'description': 'Description 2',
                       'limits': {'min': '10um',
                       'max': '20um'}
                       }
    daqs = {'DAQ 1': {
        'output': [dev1, dev2],
    },
    'DAQ 2': {
        'output': [dev2],
    }}


    app = QtGui.QApplication(sys.argv)
    window = ScanConfigWidget()
    window.populate_devices(daqs)
    window.show()
    sys.exit(app.exec_())