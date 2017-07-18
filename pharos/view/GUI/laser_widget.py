from PyQt4 import QtCore
from pharos.view.GUI.laser_widget_gui import LaserWidgetGUI


class LaserWidget(LaserWidgetGUI):
    def __init__(self, laser, parent=None):
        LaserWidgetGUI.__init__(self, parent)

        self.laser = laser  # laser class

        QtCore.QObject.connect(self, QtCore.SIGNAL('button_pressed'), self.set_parameters)

    def set_parameters(self, value, key):
        print('Setting: %s to value %s'%(key,value))
        setattr(self.laser, key, value)
        print('Laser value: %s'%getattr(self.laser, key))

    def configure_laser(self):
        laser_config = self.update_laser()
        for key in laser_config:
            self.set_parameters(laser_config[key], key)

        if self.continuous_button.isChecked():
            if self.one_button.isChecked():
                if self.trigger_check.isChecked():
                    sweep_mode = 'ContOneTrig'
                else:
                    sweep_mode = 'ContOne'
            else:
                if self.trigger_check.isChecked():
                    sweep_mode = 'ContTwoTrig'
                else:
                    sweep_mode = 'ContTwo'
        else:
            if self.one_button.isChecked():
                if self.trigger_check.isChecked():
                    sweep_mode = 'StepOneTrig'
                else:
                    sweep_mode = 'StepOne'
            else:
                if self.trigger_check.isChecked():
                    sweep_mode = 'StepTwoTrig'
                else:
                    sweep_mode = 'StepTwo'
        self.laser.sweep_mode = sweep_mode
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
