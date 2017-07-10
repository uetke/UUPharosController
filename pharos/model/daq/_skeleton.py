"""
    Pharos.Model.daq._skeleton.py
    ==================================

    .. note:: **IMPORTANT** Whatever new function is implemented in a specific model, it should be first declared in the
    laserBase class. In this way the other models will have access to the method and the program will keep running
    (perhaps with non intended behavior though).

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""


class DaqBase():
    def analog_input_setup(self, conditions):
        """Triggers an analog measurement. It does not read the value.
        conditions -- a dictionary with the needed parameters for an analog acquisition.
        """
        pass

    def trigger_analog(self, task_number):
        """Gets the analog values acquired with the triggerAnalog function.
        conditions -- dictionary with the number of points ot be read
        """
        pass

    def read_analog(self, task_number, conditions):
        """Starts continuous acquisition of the specified channels with the specified timing interval.
        conditions['devs'] -- list of devices to monitor
        conditions['accuracy'] -- accuracy for the monitor. If not defined defaults to 0.1s
        """
        pass