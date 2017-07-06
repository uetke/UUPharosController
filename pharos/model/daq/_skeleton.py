"""
    Pharos.Model.daq._skeleton.py
    ==================================

    .. note:: **IMPORTANT** Whatever new function is implemented in a specific model, it should be first declared in the
    laserBase class. In this way the other models will have access to the method and the program will keep running
    (perhaps with non intended behavior though).

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""


class DaqBase():
    TRIG_EXTERNAL = 1
    TRIG_INTERNAL = 2

    def triggerAnalog(self, conditions):
        """Triggers an analog measurement. It does not read the value.
        conditions -- a dictionary with the needed parameters for an analog acquisition.
        """
        pass

    def getAnalog(self,conditions):
        """Gets the analog values acquired with the triggerAnalog function.
        conditions -- dictionary with the number of points ot be read
        """
        pass

    def startMonitor(self,conditions):
        """Starts continuous acquisition of the specified channels with the specified timing interval.
        conditions['devs'] -- list of devices to monitor
        conditions['accuracy'] -- accuracy for the monitor. If not defined defaults to 0.1s
        """
        pass

    def readMonitor(self):
        """Reads the monitor values of all the channels specified.
        """
        pass

    def stopMonitor(self):
        """Stops all the tasks related to the monitor.
        """
        pass

    def fastTimetrace(self,conditions):
        """ Acquires a fast timetrace of the selected devices.
        conditions['devs'] -- list of devices to monitor
        conditions['accuracy'] -- accuracy in milliseconds.
        conditions['time'] -- total time of acquisition for each channel in seconds.
        """
        pass