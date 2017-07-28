# -*- coding: utf-8 -*-
"""
    pharos.controller.santec.tsl710IEEE
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Driver for the tsl710 laser, based on the manual provided, following the Command set List 2 page 7-38).
    It is compliant with IEEE-488.2.
"""

from lantz import Feat, DictFeat, Action
from lantz.errors import InvalidCommand
from pyvisa import constants
from lantz.messagebased import MessageBasedDriver

class tsl710(MessageBasedDriver):
    DEFAULTS = {'COMMON': {'read_termination': '\r\n',
                           'write_termination': '\r\n',
                           },}

    def initialize(self):
        super().initialize()

    @Feat()
    def idn(self):
        return self.query('*IDN?')

    @Feat(values={'No Error': 0,
                  'LD Temperature is out of range (at LD OFF)': 1,
                  'LD Temperature is out of range (at LD ON)': 2,
                  'Wavelength monitor temperature is out of range': 3,
                  'LD injection current is overload': 4,
                  'Power monitor is malfunction': 5})
    def self_test(self):
        return self.query('*TST?')

    @Action()
    def reset(self):
        self.write('*RST')

    @Action()
    def reboot(self):
        """ Resets the device"""
        self.write(':SPEC:REB')

    @Feat(values={'nm': 0, 'THz': 1})
    def wavelength_units(self):
        return self.query(':WAV:UNIT?')
        
    @wavelength_units.setter
    def wavelength_units(self, value):
        self.write(':WAV:UNIT {}'.format(value))
        
    @Feat(units='nm', limits=(1480, 1640, 0.0001))
    def wavelength(self):
        #self.wavelength_units = 'nm'
        return self.query(':WAV?')

    @wavelength.setter
    def wavelength(self, value):
        #self.wavelength_units = 'nm'
        self.write(':WAV %.4f' % value)

    @Feat(units='THz')
    def frequency(self):
        #self.wavelength_units = 'THz'
        return self.query(':FREQ?')

    @frequency.setter
    def frequency(self, value):
        #self.wavelength_units = 'THz'
        self.write(':FREQ %.5f' % value)

    @Feat(limits=(-100, 100, 0.01))
    def fine_tune(self):
        return self.query(':WAV:FIN?')

    @fine_tune.setter
    def fine_tune(self, value):
        self.write(':WAV:FIN %.2f' % value)

    @Action()
    def fine_tune_stop(self):
        """
        Stops fine-tuning mode and starts closed-loop wavelength controlling.
        :return:
        """
        self.write(':WAV:FIN:DIS')

    @Feat(values={'dBm': 0, 'mW': 1})
    def power_units(self):
        return self.query('POW:UNIT?')

    @power_units.setter
    def power_units(self, value):
        self.write('POW:UNIT {}'.format(value))

    @Feat(limits=(-20, 10, 0.01), units='dB')
    def powerdB(self):
        """
        Sets the optical power in dBm
        :return:
        """
        self.power_units = 'dBm'
        return self.query(':POW?')

    @powerdB.setter
    def powerdB(self, value):
        self.power_units = 'dBm'
        self.write(':POW {}'.format(value))

    @Feat(units='mW', limits=(0.01, 10, 0.01))
    def powermW(self):
        """
        sets the optical power in mW
        :return:
        """
        self.power_units = 'mW'
        return self.query(':POW?')

    @powermW.setter
    def powermW(self, value):
        self.write(':POW {}'.format(value))

    @Feat(units='mW')
    def real_power(self):
        self.power_units = 'mW'
        return self.query(':POW:ACT?')

    @Feat(units='dB', limits=(0, 30, 0.01))
    def attenuator(self):
        return self.query(':POW:ATT?')

    @attenuator.setter
    def attenuator(self, value):
        self.write(':POW:ATT %.2f' % value)

    @Feat(units='nm', limits=(1480, 1640, 0.0001))
    def stop_wavelength(self):
        """Stop sweep wavelength."""
        return self.query(':WAV:SWE:STOP?')

    @stop_wavelength.setter
    def stop_wavelength(self, value):
        self.write(':WAV:SWE:STOP %.4f' % value)

    @Feat(units='nm', limits=(1480, 1640, 0.0001))
    def start_wavelength(self):
        return self.query(':WAV:SWE:STAR?')

    @start_wavelength.setter
    def start_wavelength(self, value):
        self.write(':WAV:SWE:STAR %.4f' % value)

    @Feat(units='THz')
    def start_frequency(self):
        """Start sweep frequency."""
        return self.query(':FREQ:SWE:STAR?')

    @start_frequency.setter
    def start_frequency(self, value):
        self.write(':FREQ:SWE:STAR %.5f' % value)

    @Feat(units='THz')
    def stop_frequency(self):
        """Sweep stop frequency."""
        return self.query(':FREQ:SWE:STOP?')

    @stop_frequency.setter
    def stop_frequency(self, value):
        self.write(':FREQ:SWE:STOP %.5f' % value)

    @Feat(units='s', limits=(0, 999.9, 0.1))
    def wait_time(self):
        """Wait time between each sweep in continuous sweep operation."""
        return self.query(':WAV:SWE:DEL?')

    @wait_time.setter
    def wait_time(self, value):
        self.write(':WAV:SWE:DEL %.1f' % value)

    @Feat(units='s', limits=(0, 999.9, 0.1))
    def step_time(self):
        """Amount of time spent during each step in step sweep operation."""
        return self.query(':WAV:SWE:DWEL?')

    @step_time.setter
    def step_time(self, value):
        self.write(':WAV:SWE:DWEL %.1f' % value)

    @Feat(limits=(0, 999, 1))
    def wavelength_sweeps(self):
        """Number of wavelengths sweeps."""
        return self.query(':WAV:SWE:CYCL?')

    @wavelength_sweeps.setter
    def wavelength_sweeps(self, value):
        self.write(':WAV:SWE:CYCL %i' % value)

    @Feat(limits=(0.5, 100, 0.1))
    def wavelength_speed(self):
        """Speed for continuous sweeps (in nm/s)"""
        return self.query(':WAV:SWE:SPE?')

    @wavelength_speed.setter
    def wavelength_speed(self, value):
        self.write(':WAV:SWE:SPE %.1f' % value)

    @Feat(units='nm', limits=(0.0001, 160, 0.0001))
    def step_wavelength(self):
        """Step interval (wavelength) of step sweeps. """
        return self.query(':WAV:SWE:STEP?')

    @step_wavelength.setter
    def step_wavelength(self, value):
        self.write(':WAV:SWE:STEP %.4f' % value)

    @Feat(units='THz', limits=(0.00002, 19.76219, 0.00001))
    def step_frequency(self):
        return self.query(':FREQ:SWE:STEP?')

    @step_frequency.setter
    def step_frequency(self, value):
        self.write(':FREQ:SWE:STEP %.5f' % value)

    @Feat(values={
        'ContOne': 1,
        'ContTwo': 3,
        'StepOne': 0,
        'StepTwo': 1,
    })
    def sweep_mode(self):
        return self.query(':WAV:SWE:MOD?')

    @sweep_mode.setter
    def sweep_mode(self, value):
        self.write(':WAV:SWE:MOD %s' % value)

    @Action()
    def execute_sweep(self):
        """
        Executes sweeps or puts the device in trigger signal standby.
        The number of sweeps is defined by the method wavelength_sweeps.
        """
        self.write(':WAV:SWE 1')

    @Action()
    def pause_sweep(self):
        self.write(':WAV:SWE 2')

    @Action()
    def stop_sweep(self):
        self.write(':WAV:SWE 0')

    @Action()
    def resume_sweep(self):
        self.write(':WAV:SWE 3')

    @Action()
    def software_trigger(self):
        self.write(':WAV:SWE:SOFT')

    @Feat()
    def number_sweeps(self):
        return self.query(':WAV:SWE:COUN?')

    @Feat(values={
        'Stop': 0,
        'Executing': 1,
        'Pause': 2,
        'Awaiting trigger': 3,
        'Setting to sweep start wavelength': 4
    })
    def sweep_condition(self):
        return int(self.query(':WAV:SWE?'))

    @Feat(values={
        'None': 0,
        'Stop': 1,
        'Start': 2,
        'Step': 3
    })
    def timing_trigger(self):
        return int(self.query(':TRIG:OUTP?'))

    @timing_trigger.setter
    def timing_trigger(self, value):
        self.write(':TRIG:OUTP %i' % value)

    @Feat(units='nm', limits=(0.0001, 160, 0.0001))
    def interval_trigger(self):
        """Sets the interval of the trigger signal output."""
        return self.query(':TRIG:OUTP:STEP?')

    @interval_trigger.setter
    def interval_trigger(self, value):
        self.write(':TRIG:OUTP:STEP %.4f' % value)

    @Feat(values={True: '1', False: '0'})
    def coherent_control(self):
        return self.query(':COHC?')

    @coherent_control.setter
    def coherent_control(self, value):
        self.write(':COHC {}'.format(value))

    @Feat(values={True: '1', False: '0'})
    def LD_current(self):
        return self.query(':POW:STAT?')

    @LD_current.setter
    def LD_current(self, value):
        self.write(':POW:STAT {}'.format(value))

    @Feat(values={True: '1', False: '0'})
    def auto_power(self):
        return self.query(':POW:ATT:AUT?')

    @auto_power.setter
    def auto_power(self, value):
        self.write(':POW:ATT:AUT {}'.format(value))

    @Feat(values={True: '1', False: '0'})
    def trigger(self):
        return self.query(':TRIG:INP:EXT?')

    @trigger.setter
    def trigger(self, value):
        self.write(':TRIG:INP: {}'.format(value))

    @Feat(values={True: '1', False: '0'})
    def shutter(self):
        return self.query(':POW:SHUT?')

    @shutter.setter
    def shutter(self, value):
        self.write(':POW:SHUT {}'.format(value))
        

if __name__ == "__main__":
    with tsl710.via_gpib(1) as inst:
        print(inst.idn)
        inst.shutter = False
        print(inst.shutter)
        inst.shutter = True
        print(inst.shutter)