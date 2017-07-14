from PyQt4 import QtCore
from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI

class LaserWidget(LaserWidgetGUI):
    def __init__(self, laser, parent=None):
        LaserWidgetGUI.__init__(self, parent)

        self.laser = laser  # laser class

        QtCore.QObject.connect(self, QtCore.SIGNAL('button_pressed'), self.set_parameters)

    def set_parameters(self, value, key):
        setattr(self.laser, key, value)


if __name__ == '__main__':
    import sys
    from PyQt4.Qt import QApplication

    app = QApplication(sys.argv)
    class laserClass(object):
        pass
    laser = laserClass()
    laser.LD_current = False
    laser.shutter = False
    LW = LaserWidget(laser)
    LW.show()
    sys.exit(app.exec_())
