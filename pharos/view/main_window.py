from .GUI.mainwindow import MainWindowGUI


class MainWindow(MainWindowGUI):
    def __init__(self, session):
        MainWindowGUI.__init__(self, parent=None)
        self.laser = session.laser
        self.daq = session.daq

        #self.wavelength = self.laser.wavelength


if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    import sys
    from model.lib.session import session
    session.laser = None
    session.adq = None

    ap = QApplication(sys.argv)
    window = MainWindow(session)
    window.show()
    ap.exit(ap.exec_())