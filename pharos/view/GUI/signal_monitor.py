import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui


class SignalMonitorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=None)
        self.name = None
        self.id = None
        self.wavelength = None
        self.ydata = None
        self.starting_point = 0
        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Wavelength', units='nm')

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

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.ydata = np.zeros((len(self.wavelength)))
        self.update_monitor()

    def set_ydata(self, values):
        if len(values) + self.starting_point <= len(self.ydata):
            self.ydata[self.starting_point:self.starting_point+len(values)] = values
            self.starting_point += len(values)
            self.update_monitor()
        else:
            # Have to split the data
            self.set_ydata(values[0:len(self.ydata)-self.starting_point])
            self.starting_point = 0
            self.set_ydata(values[len(self.ydata)-self.starting_point:])
        

    def update_monitor(self):
        self.main_plot.plot(self.wavelength, self.ydata)