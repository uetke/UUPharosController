import os
from PyQt4 import uic
from PyQt4 import QtCore, QtGui
from lantz import Q_


class ShutterGui(QtGui.QWidget):
    def __init__(self, measurement=None, parent=None):
        QtGui.QWidget.__init__(self)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p,'QtCreator/shutter.ui'), self)
        self.measurement = measurement
        self.OpenButton.clicked.connect(self.measurement.open_shutter)
        self.CloseButton.clicked.connect(self.measurement.close_shutter)