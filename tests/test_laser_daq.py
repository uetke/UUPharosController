""" Test the laser and the DAQ at the same time."""

import unittest
from pharos.controller.santec.tsl710 import tsl710 as LaserController
from pharos.model.daq.ni import ni
from pharos.model.lib.device import device
from lantz import Q_
from time import sleep, time


class TestLaserDAQ(unittest.TestCase):
    def setUp(self):
        try:
            self.inst = LaserController.via_gpib(1)
            self.inst.initialize()
        except:
            self.fail('Impossible to communicate with laser')
        self.daq = ni(daq_num=2)
        dev1 = {'port': 0,
                'limits': {'min': 0, 'max': 2.5}}
        self.dev = device(dev1)
        
    def test_number_points_one(self):
        self.inst.start_wavelength = Q_('1505 nm')
        self.inst.stop_wavelength = Q_('1510 nm')
        self.inst.wavelength_speed = Q_('0.5 nm/s')
        self.inst.step_wavelength = Q_('0.01nm')
        self.inst.sweep_mode = 'ContOne'
        num_points = int((self.inst.stop_wavelength-self.inst.start_wavelength)/self.inst.step_wavelength) +1
        accuracy = self.inst.step_wavelength/self.inst.wavelength_speed
        conditions = {'devices': self.dev,
                      'accuracy': accuracy,
                      'trigger': 'external',
                      'trigger_source': 'PFI0',
                      'trigger_edge': 'falling',
                      'points': num_points,
                      'sampling': 'continuous',}
                      
        t = self.daq.analog_input_setup(conditions)
        self.daq.trigger_analog(t)
        self.inst.execute_sweep()
        #self.assertEqual(self.inst.sweep_condition, 'Executing', 'Sweep is not executing')
        approx_time=(self.inst.stop_wavelength-self.inst.start_wavelength)/self.inst.wavelength_speed
        t0 = time()
        while not self.daq.is_task_complete(t):
            sleep(0.1)
            if time()-t0>approx_time.m_as('s')*2:
                break
        
        self.daq.stop_task(t)
        conditions.update({'points': -1})
        v, d = self.daq.read_analog(t, conditions)
        self.daq.clear_task(t)
        self.assertEqual(v, num_points, 'Number of acquired points is wrong')
        
    def test_number_points_two(self):
        self.inst.start_wavelength = Q_('1509 nm')
        self.inst.stop_wavelength = Q_('1510 nm')
        self.inst.wavelength_speed = Q_('1 nm/s')
        self.inst.step_wavelength = Q_('0.001nm')
        self.inst.sweep_mode = 'ContTwo'
        num_points = int((self.inst.stop_wavelength-self.inst.start_wavelength)/self.inst.step_wavelength) +1
        num_points = num_points*2
        accuracy = self.inst.step_wavelength/self.inst.wavelength_speed
        conditions = {'devices': self.dev,
                      'accuracy': accuracy,
                      'trigger': 'external',
                      'trigger_source': 'PFI0',
                      'trigger_edge': 'rising',
                      'points': num_points,
                      'sampling': 'continuous',}
                      
        t = self.daq.analog_input_setup(conditions)
        self.daq.trigger_analog(t)
        self.inst.execute_sweep()
        #self.assertEqual(self.inst.sweep_condition, 'Executing', 'Sweep is not executing')
        approx_time=(self.inst.stop_wavelength-self.inst.start_wavelength)/self.inst.wavelength_speed*1
        t0 = time()
        while not self.daq.is_task_complete(t):
            sleep(0.1)
            if time()-t0>approx_time.m_as('s')*2:
                break
        self.daq.stop_task(t)
        conditions.update({'points': -1})
        v, d = self.daq.read_analog(t, conditions)
        self.daq.clear_task(t)
        self.assertEqual(v, num_points, 'Number of acquired points is wrong')
        
if __name__ == '__main__':
    unittest.main()