"""
    Monitor a signal with memory. This means that the latest signal will be plotted in a specific color, while older
    data will be plotted as thinner lines that fade out with time.

    Parameters to configure: The number of plots to keep in memory and the colors/thicknesses of each line.
"""
import os.path
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from scipy.optimize import leastsq

from pharos.model.lib.general_functions import lorentz, errorfunc

class MonitorMemory(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.wavelength = None
        self.two_way = False
        self.memory = 10  # Number of previous plots to save
        self.starting_point = 0

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
        self.setMenuBar(self.menu)

        self.central_widget = QtGui.QWidget()
        self.central_widget.setLayout(QtGui.QVBoxLayout())
        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Wavelength (nm)', **{'color': '#FFF', 'font-size': '14pt'})

        self.central_widget.layout().addWidget(self.main_plot)
        self.setCentralWidget(self.central_widget)

        self.p = None
        self.p1 = None
        self.p2 = None
        self.name = None
        self.id = None
        self.show_label = False
        self.do_average_plot = False
        self.lorentz_fitting = False
        self.label = pg.TextItem(border='w', fill=(0,0,255))

        self.plot_average = QtGui.QAction("Plot Average", self.main_plot.plotItem.vb.menu)
        self.plot_average.triggered.connect(self.make_average)
        self.main_plot.plotItem.vb.menu.addAction(self.plot_average)
        self.fit_lorentzian_action = QtGui.QAction("Fit a Lorentzian", self.main_plot.plotItem.vb.menu)
        self.fit_lorentzian_action.triggered.connect(self.fit_lorentzian)
        self.main_plot.plotItem.vb.menu.addAction(self.fit_lorentzian_action)
        self.directory = None

    def clear_data(self):
        self.layout.removeWidget(self.main_plot)
        self.main_plot.deleteLater()
        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Wavelength (nm)', **{'color': '#FFF', 'font-size': '14pt'})
        self.layout.addWidget(self.main_plot)
        self.ydata = None
        self.wavelength = None
        self.wavelength2 = None
        self.starting_point = 0
        self.two_way = False
        self.p1 = None
        self.p2 = None
        self.p = None

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.starting_point = 0
        if self.two_way:
            self.wavelength2 = wavelength[::-1]
            self.ydata = np.zeros((self.memory, 2*len(self.wavelength)))
            self.len_ydata = 2*int(len(self.wavelength))
            self.p1 = []
            self.p2 = []
            for i in range(self.memory):
                d1 = self.ydata[-i, :int(self.len_ydata/2)]
                d2 = self.ydata[-i, int(self.len_ydata/2):]
                self.p1.append(self.main_plot.plot(self.wavelength, d1))
                self.p1[-1].setDownsampling(auto=True, method='peak')
                self.p2.append(self.main_plot.plot(self.wavelength, d2))
                self.p2[-1].setDownsampling(auto=True, method='peak')
        else:
            self.ydata = np.zeros((self.memory, len(self.wavelength)))
            self.len_ydata = int(len(self.wavelength))
            self.p = []
            for i in range(self.memory):
                self.p.append(self.main_plot.plot(self.wavelength, self.ydata[-1, :]))
                self.p[-1].setDownsampling(auto=True, method='peak')
        self.set_pens()
        self.main_plot.scene().sigMouseMoved.connect(self.print_mouse)


    def set_ydata(self, values):
        val_len = len(values)
        if val_len + self.starting_point <= self.len_ydata:
            self.ydata[-1, self.starting_point:self.starting_point+val_len] = values
            self.starting_point += val_len
        else:
            # Have to split the data and roll the accumulation matrix
            self.set_ydata(values[0:self.len_ydata-self.starting_point])
            self.ydata = np.roll(self.ydata, -1, axis=0)
            self.starting_point = 0
            self.set_ydata(values[self.len_ydata-self.starting_point:])
        self.update_monitor()

    def update_monitor(self):
        if self.two_way:
            for i in range(self.memory):
                d1 = self.ydata[-i-1, :int(self.len_ydata/2)]
                d2 = self.ydata[-i-1, int(self.len_ydata/2):]
                self.p1[i].setData(self.wavelength, d1)
                # self.p1.setDownsampling(auto=True, method='peak')
                self.p2[i].setData(self.wavelength2, d2)
                # self.p2.setDownsampling(auto=True, method='peak')
            if self.do_average_plot:
                data_mean = np.mean(self.ydata, axis=0)
                self.p1[0].setData(self.wavelength, data_mean[:int(self.len_ydata/2)])
                self.p2[0].setData(self.wavelength, data_mean[int(self.len_ydata/2):])
        else:
            for i in range(self.memory):
                d = self.ydata[-i-1, :]
                self.p[i].setData(self.wavelength, d)
            if self.do_average_plot:
                data_mean = np.mean(self.ydata, axis=0)
                for i in range(self.memory - 1):
                    self.p[i].setPen({'color': '#b6dbff', 'width': .1})
                self.p[-1].setData(self.wavelength, data_mean)
                self.p[-1].setPen({'color': '#b6dbaa', 'width': 5})

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

    def save(self):
        if self.directory is not None:
            i = 0
            filename = 'monitor_data_'
            while os.path.isfile(os.path.join(self.directory, '%s%i.dat' % (filename, i))):
                i += 1
            file = os.path.join(self.directory, '%s%i.dat' % (filename, i))
            header = "# Data saved by Pharos Controller\n"

            with open(file, 'wb') as f:
                if not self.two_way:
                    header += "# Column 1: Wavelength, Column 2-{}: {}\n".format(self.memory, self.name)
                    data = np.vstack((self.wavelength, self.ydata))
                else:
                    header += "# Column 1: Wavelength, Column 2 - {}: {} forward, Column {}-{}: {} backward\n".format(self.memory, self.name, self.memory+1, self.memory*2, self.name)
                    d1 = self.ydata[:, :int(self.len_ydata/2)]
                    d2 = self.ydata[:, int(self.len_ydata/2):]
                    data = np.vstack((self.wavelength, d1, d2))
                f.write(header.encode('ascii'))
                np.savetxt(f, data.T, fmt='%7.5f')
            print('Data saved to %s' % file)
        else:
            self.choose_dir()

    def choose_dir(self):
        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        self.save()

    def print_mouse(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        vb = self.main_plot.plotItem.vb
        x = vb.mapSceneToView(event).x()
        y = vb.mapSceneToView(event).y()
        self.x_mouse = x
        self.y_mouse = y

        if modifiers == QtCore.Qt.ControlModifier:
            if not self.show_label:
                self.show_label = True
                self.label.show()
                self.main_plot.addItem(self.label)
            self.label.setPos(vb.mapSceneToView(event))
            self.label.setHtml("<span style='font-size: 12pt'>x=%0.1f</span> <br />   <span style='font-size: 12pt'>y1=%0.1f</span>" % (
                x, y))
        else:
            if self.show_label:
                self.label.hide()
                self.show_label = False

    def set_pens(self):
        if self.do_average_plot:
            if self.two_way:
                for i in range(self.memory):
                    self.p1[i].setPen({'color': '#b6dbff', 'width': .1})
                    self.p2[i].setPen({'color': '#ffff6d', 'width': .1})
                self.p1[0].setPen({'color': '#b6dbff', 'width': 3})
                self.p2[0].setPen({'color': '#ffff6d', 'width': 3})
            else:
                for i in range(self.memory):
                    self.p[i].setPen({'color': '#b6dbff', 'width': .1})
                self.p[0].setPen({'color': '#b6dbff', 'width': 3})
        else:
            if self.two_way:
                for i in range(self.memory):
                    self.p1[i].setPen({'color': '#b6dbff', 'width': 1/(i+1)})
                    self.p2[i].setPen({'color': '#ffff6d', 'width': 1/(i+1)})
                self.p1[-1].setPen({'color': '#b6dbff', 'width': 3})
                self.p2[-1].setPen({'color': '#ffff6d', 'width': 3})
            else:
                for i in range(self.memory):
                    self.p[i].setPen({'color': '#b6dbff', 'width': 1/(i+1)})
                self.p[-1].setPen({'color': '#b6dbff', 'width': 3})

    def make_average(self):
        if not self.do_average_plot:
            self.do_average_plot = True
            self.set_pens()
            self.update_monitor()
        else:
            self.do_average_plot = False
            self.set_pens()
            self.update_monitor()

    def fit_lorentzian(self):

        if not self.lorentz_fitting:
            self.lorentz_fitting = True
            if self.do_average_plot:
                data = np.mean(self.ydata, axis=0)
            else:
                data = self.ydata[-1, :]

            if self.two_way:
                d1 = data[:int(self.len_ydata/2)]
                d2 = data[int(self.len_ydata/2):]
                p0 = [self.y_mouse-np.min(d1), self.x_mouse, 1, np.min(d1)]
                solp1, ier = leastsq(errorfunc,
                                     p0,
                                     args=(self.wavelength, d1),
                                     Dfun=None,
                                     full_output=False,
                                     ftol=1e-9,
                                     xtol=1e-9,
                                     maxfev=100000,
                                     epsfcn=1e-10,
                                     factor=0.1)
                self.lorentz_plot1 = self.main_plot.plot(self.wavelength, lorentz(solp1, self.wavelength))

                p0 = [self.y_mouse - np.min(d2), self.x_mouse, 1, np.min(d2)]
                solp2, ier = leastsq(errorfunc,
                                     p0,
                                     args=(self.wavelength2, d2),
                                     Dfun=None,
                                     full_output=False,
                                     ftol=1e-9,
                                     xtol=1e-9,
                                     maxfev=100000,
                                     epsfcn=1e-10,
                                     factor=0.1)

                self.lorentz_plot2 = self.main_plot.plot(self.wavelength, lorentz(solp2, self.wavelength))

            else:
                p0 = [self.y_mouse - np.min(data), self.x_mouse, 1, np.min(data)]
                solp, ier = leastsq(errorfunc,
                                     p0,
                                     args=(self.wavelength, data),
                                     Dfun=None,
                                     full_output=False,
                                     ftol=1e-9,
                                     xtol=1e-9,
                                     maxfev=100000,
                                     epsfcn=1e-10,
                                     factor=0.1)
                self.lorentz_plot = self.main_plot.plot(self.wavelength, lorentz(solp, self.wavelength))

if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication

    wavelength = np.linspace(1492, 1512, 500)
    ap = QApplication(sys.argv)
    m = MonitorMemory()
    m.memory = 1
    m.two_way = True
    m.set_wavelength(wavelength)
    m.set_name('Test')
    d1 = lorentz([1, 1505, 3, 4], wavelength)
    d2 = lorentz([5, 1500, 2.5, 3.4], wavelength)
    m.set_ydata(d1)
    m.set_ydata(d2)
    # for _ in range(5):
    #     data = np.random.random(500)
    #     m.set_ydata(data)
    #
    m.show()
    ap.exit(ap.exec_())