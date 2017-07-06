import sys

from pyqtgraph.Qt import QtGui, QtCore


from .QtCreator.LaserWidget.widget import Ui_Form

class LaserWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == '__main__':
    from PyQt4.Qt import QApplication
    app = QApplication(sys.argv)
    mon = LaserWidget()
    mon.show()
    sys.exit(app.exec_())
