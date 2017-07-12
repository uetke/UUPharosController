import pyqtgraph as pg
from pyqtgraph.Qt import QtGui


class SignalMonitorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=None)
        self.name = None
        self.id = None

        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Time', units='s')

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.main_plot)

    def set_name(self, name):
        if self.name is not None:
            raise Exception('Cannot change the name of a running window.')
        else:
            self.name = name
            self.setWindowTitle(name)

    def set_id(self, id):
        if self.id is not None:
            raise Exception('Cannot change the id a running window.')
        else:
            self.id = id