"""
    Pharos.Model.daq.ni.py
    ==================================
    National Instruments model for acquiring analog signals.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
import PyDAQmx as nidaq
import numpy as np
from _skeleton import DaqBase
from lantz import Q_

class ni(DaqBase):

    def __init__(self, adq_num=1):
        """Class trap for condensing tasks that can be used for interacting with an optical trap.
        session -- class with important variables, including the adq card.
        """
        self.running = False
        self.adq_num = adq_num
        self.monitorNum = []
        self.tasks = []

    def analog_input_setup(self, conditions):
        """
        Sets up a task for acquaring a number of analog channels.
        conditions -- dictionary with the needed conditions to set up an acquisition.

        """
        t = nidaq.Task()
        dev = 'Dev%s' % self.deviceNumber
        if not isinstance(conditions['devices'], list):
            channel = ["Dev%s/ai%s" % (self.adq_num, dev.port)]
            limit_min = [dev.limit[0]]
            limit_max = [dev.limit[1]]
        else:
            channel = []
            limit_max = []
            limit_min = []
            for dev in devs:
                channel.append("Dev%s/ai%s" % (self.adq_num, dev.port))
                limit_min.append(dev.limit[0])
                limit_max.append(dev.limit[1])

        channels = ', '.join(channel)
        channels.encode('utf-8')
        freq = 1/conditions['accuracy'].to('s')
        if conditions['trigger'] == 'external':
            trigger = "Dev%s/%s" % (self.adq_num,conditions['trigger_source'])
        else:
            trigger = ""
        if 'trigger_edge' in conditions:
            if conditions['trigger_edge'] == 'rising':
                trigger_edge = nidaq.DAQmx_Val_Rising
            elif conditions['trigger_edge'] == 'falling':
                trigger_edge = nidaq.DAQmx_Val_Falling
        else:
            trigger_edge = nidaq.DAQmx_Val_Rising

        t.CreateAIVoltageChan(channels, None, nidaq.DAQmx_Val_RSE, min(limit_min),
                              max(limit_max), nidaq.DAQmx_Val_Volts, None)

        if conditions['points'] > 0:
            cont_finite = nidaq.DAQmx_Val_FiniteSamps
        else:
            cont_finite = nidaq.DAQmx_Val_ContSamps

        t.DAQmxCfgSampClkTiming(trigger, freq.magnitude, trigger_edge, cont_finite, conditions['points'])
        self.tasks.append(t)
        return len(self.tasks)-1

    def trigger_analog(self, task):
        """
        :param task: Task number to be triggered.
        :return:
        """
        t = self.tasks[task]
        t.StartTask()  # Starts the measurement.
        self.running = True


    def read_analog(self, task, conditions):
        """Gets the analog values acquired with the triggerAnalog function.
        conditions -- dictionary with the number of points ot be read
        """

        t = self.tasks[task]

        read = nidaq.int32()
        points = int(conditions['points'])
        if points > 0:
            data = np.zeros((points,), dtype=np.float64)
            t.ReadAnalogF64(points, .2, nidaq.DAQmx_Val_GroupByChannel,
                            data, points, nidaq.byref(read), None)
        else:
            data = np.zeros((10000,), dtype=np.float64)
            t.ReadAnalogF64(points, .2, nidaq.DAQmx_Val_GroupByChannel,
                            data, points, nidaq.byref(read), None)
        values = read.value
        return values, data



if __name__ == '__main__':
    a = ni()
    b = 10*Q_('ms')
    print(type(b))
    # b = Q_(b, 'seconds')
    print(1/b.to('seconds'))
    print(nidaq.DAQmx_Val_Falling)
    print(b.magnitude)
