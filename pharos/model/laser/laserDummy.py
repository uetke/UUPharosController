"""
    Pharos.Model.laser.dummyCamera.py
    ====================================
    Dummy camera class for testing GUI and other functionalities. Based on the skeleton.

    .. sectionauthor: Aquiles Carattino <aquiles@uetke.com>
"""

from ._skeleton import LaserBase

class DummyLaser(LaserBase):
    def __init__(self, laser_no):
        self.laser = laser_no  # Laser number (to communicate via serial, etc.)
        self.running_scan = False

    def wavelength_scan_setup(self, start, end, steps, time, trigger, mode):
        self.parameter = self.PARAM_WAVELENGTH
        self.start = start
        self.end = end
        self.steps = steps
        self.time = time
        self.triger = trigger
        self.mode = mode

    def frequency_scan_setup(self, start, end, steps, time, trigger, mode):
        self.parameter = self.PARAM_FREQUENCY
        self.start = start
        self.end = end
        self.steps = steps
        self.time = time
        self.trigger = trigger
        self.mode = mode

    def trigger_scan(self):
        if self.trigger == self.TRIG_SOFTWARE:
            print('Triggering scan via software... ')
            self.running_scan = True
        elif self.trigger == self.TRIG_EXTERNAL:
            print('Laser idle waiting for external trigger')
        elif self.trigger == self.TRIG_OUTPUT:
            print('Triggering scan via software and setting output trigger')
            self.running_scan = True


    def is_running(self):
        return self.running_scan

    def stop_scan(self):
        self.running_scan = False