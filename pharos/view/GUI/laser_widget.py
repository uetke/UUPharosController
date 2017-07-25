from PyQt4 import QtCore
from lantz import Q_
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

    def get_parameters_monitor(self):
        """ Outputs a dictionary of parameters to update the laser.
        Several assumpions are made regarding the experiment (triggers, etc.)"""
        params = {
            'start_wavelength': Q_(self.start_wavelength_line.text()),
            'stop_wavelength': Q_(self.stop_wavelength_line.text()),
            'interval_trigger': Q_(self.trigger_step_line.text()),
        }
        return params



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
