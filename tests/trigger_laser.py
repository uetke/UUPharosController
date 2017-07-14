from pharos.controller.santec.tsl710 import tsl710 as LaserController
from lantz import Q_
from time import sleep
import sys

with LaserController.via_gpib(1) as inst:
    if len(sys.argv) == 1:
        inst.pause_sweep()
        inst.stop_sweep()
        inst.disable_trigger()
        inst.coherent_control_on()
        inst.lo()
        inst.open_shutter()
        print(inst.idn)
        inst.wavelength = Q_('1510 nm')
        inst.start_wavelength = Q_('1530 nm')
        inst.stop_wavelength = Q_('1545 nm')
        inst.step_time = Q_('1 ms')
        inst.wavelength_sweeps = 1
        inst.sweep_mode = 'ContOne'
        inst.wavelength_speed = 2
        inst.trigger_timing = 'Step'
        inst.interval_trigger = 0.002 * Q_('nm')
        inst.execute_sweep()
    else:
        if sys.argv[1] == '-c':
            inst.close_shutter()
        else:
            inst.open_shutter()