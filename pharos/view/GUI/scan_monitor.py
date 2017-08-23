import os.path
from builtins import bool

import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui


class ScanMonitorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent=None)
        self.name = None
        self.id = None
        self.wavelength = None
        self.y_axis = None
        self.data = None
        self.pos = [0, 0]
        self.accuracy = [1, 1]
        self.starting_point = 0
        self.y_pos = 0
        self.menu = QtGui.QMenuBar(self)

        self.main_plot = None

        self.layout = QtGui.QHBoxLayout(self)

        self.two_way = False  # If the laser scan is two-ways

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

    def set_axis(self, axis):
        """Sets the axis names, limits and an initial empty dataset."""
        self.clear_data()

        self.wavelength = axis['wavelength']
        units_wl = self.wavelength['stop'].u  # units
        num_wl_points = ((self.wavelength['stop']-self.wavelength['start'])/self.wavelength['step']).to('')
       
        num_wl_points = int(num_wl_points.m)
        self.num_wl_points = num_wl_points
        self.y_axis = axis['y_axis']
        units_y = self.y_axis['stop'].u
        num_y_points = ((self.y_axis['stop']-self.y_axis['start'])/self.y_axis['step']).to('')
        num_y_points = int(num_y_points.m)
        self.num_y_points = num_y_points
        plt = pg.PlotItem(labels={'bottom': ('Wavelength', units_wl), 'left': (self.y_axis['name'], units_y)})
        plt.setAspectLocked(False)
        self.pos = [self.wavelength['start'].m, self.y_axis['start'].m]
        self.accuracy = [self.wavelength['step'].m, self.y_axis['step'].m]

        if self.two_way:
            self.data = np.zeros((2*num_wl_points*num_y_points))

            self.main_plot1 = pg.ImageView(view=plt)
            self.main_plot2 = pg.ImageView(view=plt)

            self.layout.addWidget(self.main_plot1)
            self.layout.addWidget(self.main_plot2)
            d1 = self.data[:self.data.shape[0]/2]
            d1 = np.reshape(d1,(num_wl_points, num_y_points))
            d2 = self.data[self.data.shape[0]/2:]
            d2 = np.reshape(d1,(num_wl_points, num_y_points))

            self.main_plot1.setImage(d1, pos=self.pos, scale=self.accuracy)
            self.main_plot2.setData(d2[::-1], pos=self.pos, scale=self.accuracy)
        else:
            self.data = np.zeros((num_wl_points*num_y_points))
            self.main_plot = pg.ImageView(view=plt)
            self.layout.addWidget(self.main_plot)
            d = np.reshape(self.data,(self.num_wl_points, self.num_y_points))
            self.main_plot.setImage(d, pos=self.pos, scale=self.accuracy)

    def clear_data(self):

        # Tries to clear all the plots. Avoids verifying if the window is running for second time.
        try:
            self.layout.removeWidget(self.main_plot1)
            self.main_plot1.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.main_plot2)
            self.main_plot2.deleteLater()
        except:
            pass
        try:
            self.layout.removeWidget(self.main_plot)
            self.main_plot.deleteLater()
        except:
            pass

        self.wavelength = None
        self.y_axis = None
        self.data = None
        self.starting_point = 0
        self.y_pos = 0
        self.two_way = False
        self.pos = [0, 0]
        self.accuracy = [1, 1]

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

    def set_data(self, values):
        if self.two_way:
            pass
        else:
            self.data[self.starting_point:self.starting_point+len(values)] = values
            self.starting_point += len(values)
            self.update_image()
        #print('Y-pos: {}'.format(self.y_pos))
        #if len(values) + self.starting_point <= self.data.shape[0]:
        #    self.data[self.starting_point:self.starting_point+len(values), self.y_pos] = values
        #    self.starting_point += len(values)
        #    self.update_image()
        #else:
        #    # Have to split the data
        #    self.set_data(values[0:self.data.shape[0]-self.starting_point])
        #    self.starting_point = 0
        #    self.y_pos += 1
        #    self.set_data(values[self.data.shape[0]-self.starting_point:])

    def update_image(self):
        if self.two_way:
            d1 = self.data[:self.data.shape[0], :]
            d2 = self.data[self.data.shape[0]:, :]

            self.main_plot1.setImage(d1)
            self.main_plot2.setData(d2[::-1])
        else:
            d = np.reshape(self.data,(self.num_wl_points, self.num_y_points))
            self.main_plot.setImage(d)

    def save(self):
        """Save the data to disk.
        This  has to be done for scans! The code was copied from the monitor.
        """

        if self.directory is not None:
            i = 0
            filename = 'scan_data_'
            while os.path.isfile(os.path.join(self.directory, '%s%i.dat' % (filename, i))):
                i += 1
            file = os.path.join(self.directory, '%s%i.dat' % (filename, i))
            if not self.two_way:
                data = np.vstack((self.wavelength, self.data))
            else:
                pass
            np.savetxt(file, data)
            print('Data seved to %s' % file)
        else:
            self.choose_dir()

    def choose_dir(self):
        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        self.save()