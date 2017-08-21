import os
from PyQt4 import QtGui, uic

class LaserScanWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'QtCreator/laser_scan_widget.ui'), self)