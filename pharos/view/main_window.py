
from GUI.mainwindow import MainWindowGUI


class MainWindow(MainWindowGUI):
    def __init__(self, _session):
        MainWindowGUI.__init__(self, parent=None)
        self.laser = _session['laser']
        self.adq = _session['adq']

        self.wavelength = self.laser.wavelength


if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    import sys
    session = {'laser': None,
                'adq': None}

    ap = QApplication(sys.argv)
    window = MainWindow(session)
    window.show()
    ap.exit(ap.exec_())