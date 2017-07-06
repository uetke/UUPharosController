"""
    Pharos.Model.laser._skeleton.py
    ==================================

    .. note:: **IMPORTANT** Whatever new function is implemented in a specific model, it should be first declared in the
    laserBase class. In this way the other models will have access to the method and the program will keep running
    (perhaps with non intended behavior though).

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""


class LaserBase():

    # Trigger modes
    TRIG_NO = 0
    TRIG_EXTERNAL = 1
    TRIG_SOFTWARE = 2
    TRIG_OUTPUT = 3

    # Scan modes
    MODE_SINGLE = 1
    MODE_TWO_WAY = 2
    MODE_STEP_SINGLE = 3
    MODE_STEP_TWO_WAY = 4

    # Parameters (wavelength or frequency)
    PARAM_WAVELENGTH = 1
    PARAM_FREQUENCY = 2

    def __init__(self):
        self.trig_mode = self.TRIG_NO # Means the trigger was not set.

    def wavelength_scan_setup(self, start, end, steps, time, trigger, mode):
        pass

    def frequency_scan_setup(self, start, end, steps, time, trigger, mode):
        pass

    def trigger_scan(self):
        pass

    def is_running(self):
        pass

    def stop_scan(self):
        pass