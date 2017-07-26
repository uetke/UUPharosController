import os
from PyQt4 import QtCore, QtGui, uic
from lantz import Q_
from PyQt4.QtCore import pyqtSlot

class ScanConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/monitor_config.ui'), self)

        self.groupbox = []
        self.devices = {}

    def populate_daq_devices(self, daqs):
        """ Adds group boxes for all the output devices connected to the daqs.
        :param daqs: Dictionary of daqs containing the devices connected Check the measurement class for the definition."""
        for d in daqs:
            self.groupbox.append(QtGui.QGroupBox())
            self.groupbox[-1].setTitle(d)
            layout = QtGui.QGridLayout()
            i = 0
            for dev in daqs[d]['output']:
                device_name = dev.properties['name']
                device_description = dev.properties['description']

                tick = QtGui.QCheckBox()
                max = QtGui.QLineEdit(dev.properties['limits']['max'])
                min = QtGui.QLineEdit(dev.properties['limits']['min'])
                step = QtGui.QLineEdit()
                # min_line.editingFinished.connect(lambda: self.check_limits(device_name, min_line.text()))
                self.devices[device_name] = {
                    'tick': tick,
                    'max_line': max,
                    'min_line': min,
                    'step_line': step,
                    'max': dev.properties['limits']['max'],
                    'min': dev.properties['limits']['min'],
                }

                min.editingFinished.connect(self.check_limits)
                max.editingFinished.connect(self.check_limits)
                step.editingFinished.connect(self.check_limits)

                label = QtGui.QLabel(device_name)
                label.setToolTip(device_description)

                layout.addWidget(tick, i, 0)
                layout.addWidget(label, i, 1)
                layout.addWidget(min, i, 2)
                layout.addWidget(max, i, 3)
                layout.addWidget(step, i, 4)

                i += 1

            self.groupbox[-1].setLayout(layout)
            self.layout_widgets.addRow(self.groupbox[-1])

    def populate_other_devices(self, devs):
        """ Adds group boxes for every device and includes the parameters that can be tuned in every case. """

    def check_limits(self):
        red_background =  "QLineEdit { background: rgb(255, 20, 20); selection-background-color: rgb(233, 99, 0); }"
        white_background = "QLineEdit { background: rgb(255, 255, 255); selection-background-color: rgb(233, 99, 0); }"
        for dev in self.devices:
            dev = self.devices[dev]
            if Q_(dev['min']) <= Q_(dev['min_line'].text()) <= Q_(dev['max']):
                dev['min_line'].setStyleSheet(white_background)
            else:
                dev['min_line'].setStyleSheet(red_background)
            if Q_(dev['min']) <= Q_(dev['max_line'].text()) <= Q_(dev['max']):
                dev['max_line'].setStyleSheet(white_background)
            else:
                dev['max_line'].setStyleSheet(red_background)



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
    window.populate_daq_devices(daqs)
    window.show()
    sys.exit(app.exec_())