import os.path
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

        self.two_way = False  # If the laser scan is two-ways

        self.menu = QtGui.QMenuBar(self)
        self.file_menu = self.menu.addMenu("&File")
        self.save_action = QtGui.QAction("&Save", self)
        self.save_action.setShortcut('Ctrl+O')
        self.save_action.triggered.connect(self.choose_dir)
        self.file_menu.addAction(self.save_action)

        self.quick_save_action = QtGui.QAction("&Quick save", self)
        self.quick_save_action.triggered.connect(self.save)
        self.quick_save_action.setShortcut('Ctrl+S')
        self.file_menu.addAction(self.quick_save_action)

        self.directory = None

    def clear_data(self):
        self.layout.removeWidget(self.main_plot)
        self.main_plot.deleteLater()
        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Wavelength', units='nm')
        self.layout.addWidget(self.main_plot)
        self.ydata = None
        self.wavelength = None
        self.starting_point = 0
        self.two_way = False
        self.p1 = None
        self.p2 = None

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
        if self.two_way:
            self.ydata = np.zeros((2*len(self.wavelength)))
            self.len_ydata = int(len(self.ydata)/2)
            d1 = self.ydata[:self.len_ydata]
            d2 = self.ydata[self.len_ydata:]
            self.p1 = self.main_plot.plot(self.wavelength, d1, pen={'color': "#b6dbff", 'width': 2})
            self.p2 = self.main_plot.plot(self.wavelength, d2, pen={'color': "#ffff6d", 'width': 2})
        else:
            self.ydata = np.zeros((len(self.wavelength)))
            self.p = self.main_plot.plot(self.wavelength, self.ydata, pen={'color': "#b6dbff", 'width': 2})

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
        if self.two_way:
            d1 = self.ydata[:self.len_ydata]
            d2 = self.ydata[self.len_ydata:]
            self.p1.setData(self.wavelength, d1)
            self.p2.setData(self.wavelength, d2[::-1])
        else:
            self.p.setData(self.wavelength, self.ydata)

    def save(self):
        if self.directory is not None:
            i = 0
            filename = 'data_'
            while os.path.isfile(os.path.join(self.directory,'%s%i.dat' % (filename, i))):
                i+=1
            file = os.path.join(self.directory,'%s%i.dat' % (filename, i))
            data = np.vstack((self.wavelength, self.ydata))
            np.savetxt(file, data)
            print('Data seved to %s' % file)
        else:
            self.choose_dir()

    def choose_dir(self):
        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        self.save()
