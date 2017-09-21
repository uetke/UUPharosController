import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from lantz import Q_

class ThorlabsRotationWidgetGUI(QtGui.QWidget):
    def __init__(self, rotation_stage, parent=None):
        QtGui.QWidget.__init__(self)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p,'QtCreator/ThorlabsRotation.ui'), self)
        self.stage = rotation_stage
        self.home_button.clicked.connect(self.home)
        self.go_button.clicked.connect(self.go_to)

        self.update_timer = QtCore.QTimer()
        self.update_timer.start(1000)
        self.update_timer.timeout.connect(self.update_position)

    def home(self):
        self.stage.driver.home_device()

    def update_position(self):
        self.curr_position.setText("{0:f~}".format(self.stage.driver.position))

    def go_to(self):
        new_pos = Q_(self.go_to_pos.text())
        self.stage.driver.position = new_pos

if __name__ == "__main__":
    import sys
    from PyQt4.Qt import QApplication
    from pharos.controller.thorlabs.tdc001 import TDC011

    os.environ['PATH'] = os.environ['PATH'] + ';' + 'C:\\Program Files (x86)\\Thorlabs\\Kinesis'
    rot = TDC011("83843619")
    ap = QApplication(sys.argv)
    m = ThorlabsRotationWidgetGUI(rot)
    m.show()
    ap.exit(ap.exec_())