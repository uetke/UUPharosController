"""
    Monitor a signal with memory. This means that the latest signal will be plotted in a specific color, while older
    data will be plotted as thinner lines that fade out with time.

    Parameters to configure: The number of plots to keep in memory and the colors/thicknesses of each line.
"""
import os.path
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtGui


class MonitorMemory(pg.GraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.wavelength = None
        self.two_way = False
        self.memory = 10  # Number of previous plots to save
        self.starting_point = 0

        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Wavelength (nm)', **{'color': '#FFF', 'font-size': '14pt'})
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.main_plot)
        # self.addWidget(self.main_plot)
        self.p = None
        self.p1 = None
        self.p2 = None
        self.name = None
        self.id = None
        # self.p.setLabel(axis='left', text='Test', units='Test U', **{'color': '#FFF', 'font-size': '14pt'})

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
                self.p1.append(self.main_plot.plot(self.wavelength, d1, pen={'color': '#b6dbff', 'width': 4/(i+1)}))
                # self.p1.setDownsampling(auto=True, method='peak')
                self.p2.append(self.main_plot.plot(self.wavelength, d2, pen={'color': '#ffff6d', 'width': 4/(i+1)}))
                # self.p2.setDownsampling(auto=True, method='peak')
        else:
            self.ydata = np.zeros((self.memory, len(self.wavelength)))
            self.len_ydata = int(len(self.wavelength))
            self.p = []
            for i in range(self.memory):
                self.p.append(self.main_plot.plot(self.wavelength, self.ydata[-1, :], pen={'color': "#b6dbff", 'width': 4/(i+1)}))
            # self.p.setDownsampling(auto=True, method='peak')

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
        else:
            for i in range(self.memory):
                d = self.ydata[-i-1, :]
                self.p[i].setData(self.wavelength, d)

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

if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication

    wavelength = np.linspace(1492, 1512, 500)
    ap = QApplication(sys.argv)
    m = MonitorMemory()
    m.set_wavelength(wavelength)
    for _ in range(20):
        data = np.random.random(500)
        m.set_ydata(data)
    m.show()
    ap.exit(ap.exec_())