from PyQt4 import QtCore
from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI


class LaserWidget(LaserWidgetGUI):
    def __init__(self, laser, parent=None):
        LaserWidgetGUI.__init__(self, parent)

        self.laser = laser  # laser class

    def configure_laser(self):
        values = self.update_laser_values()

        self.laser.update(values)

        points = int((self.laser.stop_wavelength - self.laser.start_wavelength) / self.laser.trigger_step)
        accuracy = self.laser.trigger_step/self.laser.speed

        conditions = {'points': points,
                      'accuracy': accuracy
                      }
        self.emit(QtCore.SIGNAL('configure_monitor'), conditions)



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
