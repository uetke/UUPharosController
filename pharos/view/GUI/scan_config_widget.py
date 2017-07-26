import os
from PyQt4 import QtCore, QtGui, uic


class ScanConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/monitor_config.ui'), self)

        self.groupbox = []
        self.devices = {}

    def populate_daq_devices(self, daqs):
        for d in daqs:
            self.groupbox.append(QtGui.QGroupBox())
            self.groupbox[-1].setTitle(d)
            layout = QtGui.QGridLayout()
            i = 0
            for dev in daqs[d]['output']:
                device_name = dev.properties['name']
                device_description = dev.properties['description']

                tick = QtGui.QCheckBox()
                min_line = QtGui.QLineEdit()
                max_line = QtGui.QLineEdit()
                step_line = QtGui.QLineEdit()

                inputs = {
                    'tick': tick,
                    'max': max_line,
                    'min': min_line,
                    'step': step_line,
                }

                self.devices.update(inputs)

                label = QtGui.QLabel(device_name)
                label.setToolTip(device_description)

                layout.addWidget(self.ticks[-1], i, 0)
                layout.addWidget(label, i, 1)
                layout.addWidget(min_line, i, 2)
                layout.addWidget(max_line, i, 3)
                layout.addWidget(step_line, i, 4)

                QtCore.QObject.connect(min_line, QtCore.SIGNAL('editingFinished()'), lambda: self.check_limits(device_name, min_line.text()))

                i+=1

            self.groupbox[-1].setLayout(layout)
            self.layout_widgets.addRow(self.groupbox[-1])

    def check_limits(self, dev, text):
        print(dev)
        print(text)

if __name__ == "__main__":
    class dev:
        pass
    dev1 = dev()
    dev1.properties = {'name': "Name 1",
            "description": "Description 1"}
    dev2 = dev()
    dev2.properties = {'name': 'Name 2',
                       'description': 'Description 2'}

    daqs = {}

    daqs['DAQ 1'] = {
        'output': [dev1, dev2],
    }

    import sys

    app = QtGui.QApplication(sys.argv)
    window = ScanConfigWidget()
    window.populate_daq_devices(daqs)
    window.show()
    sys.exit(app.exec_())