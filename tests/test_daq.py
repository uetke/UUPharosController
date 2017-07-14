import unittest
from pharos.model.daq.ni import ni
from pharos.model.lib.device import device
from lantz import Q_
from time import sleep, time
import PyDAQmx as nidaq

if __name__ == "__main__":
    daq = ni(daq_num=2)
    dev1 = {'port': 0,
            'limits': {'min': 0, 'max': 2.5}}
    dev = device(dev1)
    conditions = {'devices': dev,
                  'accuracy': Q_('1.5 s')/7500,
                  'trigger': 'external',
                  'trigger_source': 'PFI0',
                  'trigger_edge': 'falling',
                  'measure_mode': nidaq.DAQmx_Val_Diff,
                  'points': 7500}
    ###############################################################
    # DAQmx_Val_RSE        - Referenced Single - Ended.
    # DAQmx_Val_NRSE       - Non - Referenced Single - Ended.
    # DAQmx_Val_Diff       - Differential.
    # DAQmx_Val_PseudoDiff - Pseudodifferential.
    ###############################################################

    t = daq.analog_input_setup(conditions)
    daq.trigger_analog(t)
    print('waiting')
    t0 = time()
    while not daq.is_task_complete(t):
        sleep(0.1)
    
    print('Took: %2f s' % (time()-t0))

    v, d = daq.read_analog(t, conditions)
    print('v:')
    print(v)
    print('data:')
    print(d)