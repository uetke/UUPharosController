from PyQt4 import QtGui


class ScanConfigWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.groupbox_layout = QtGui.QVBoxLayout()
        self.groupbox = []
        self.ticks = []

    def populate_daq_devices(self, daqs):
        for d in daqs:
            self.groupbox.append(QtGui.QGroupBox())
            self.groupbox[-1].setTitle(d)
            layout = QtGui.QGridLayout()
            for dev in daqs[d]['output']:
                self.ticks.append(QtGui.QCheckBox())
                device_name = dev.properties['name']
                device_description = dev.properties['description']
                label = QtGui.QLabel(device_name)
                label.setToolTip(device_description)
                layout.addItem(self, label)
                layout.addItem(self, self.ticks[-1])
            self.groupbox[-1].setLayout(layout)
            self.groupbox_layout.addWidget(self.groupbox[-1])


if __name__ == "__main__":
    class dev:
        pass
    dev1 = dev()
    dev1.properties = {'name': "Name 1",
            "description": "Description 1"}

    daqs = {}

    daqs['DAQ 1'] = {
        'output': [dev1],
    }

    import sys

    app = QtGui.QApplication(sys.argv)
    window = ScanConfigWidget()
    window.populate_daq_devices(daqs)
    window.show()
    sys.exit(app.exec_())