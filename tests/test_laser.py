import unittest
from pharos.controller.santec.tsl710 import tsl710 as LaserController
from lantz import Q_


class TestLaser(unittest.TestCase):
    def setUp(self):
        try:
            self.inst = LaserController.via_gpib(1)
            self.inst.initialize()
        except:
            self.fail('Impossible to communicate with laser')

    def test_connection(self):
        idn = self.inst.idn
        self.assertIsInstance(idn, str, 'Identifier is not a string')

    def test_reading_values(self):
        wavelength = self.inst.wavelength
        start_wavelength = self.inst.start_wavelength

        self.assertIsInstance(wavelength, Q_, 'Wavelength is not a quantity')
        self.assertIsInstance(start_wavelength, Q_, 'Start wavelength is not a quantity')

    def test_setting_values(self):
        self.inst.wavelength = Q_('1500 nm')
        self.assertEqual(self.inst.wavelength, Q_('1500 nm'))

        self.inst.start_wavelength = Q_('1492 nm')
        self.assertEqual(self.inst.start_wavelength, Q_('1492 nm'))
        self.inst.stop_wavelength = Q_('1512 nm')
        self.assertEqual(self.inst.stop_wavelength, Q_('1512 nm'))
        self.inst.step_time = Q_('0.1 s')
        self.assertEqual(self.inst.step_time, Q_('0.1 s'))
        self.inst.step_wavelength = Q_('0.1 nm')
        self.assertEqual(self.inst.step_wavelength, Q_('0.1 nm'))
        self.inst.sweep_mode = 'StepOne'
        self.assertEqual(self.inst.sweep_mode, 'StepOne')

        self.inst.wavelength = Q_('1510 nm')
        self.assertEqual(self.inst.wavelength, Q_('1510 nm'))

    def test_triggering_actions(self):
        try:
            self.inst.coherent_control_on()
        except:
            self.fail('Couldn\'t set the coherent control')
        try:
            self.inst.lo()
        except:
            self.fail('Couldn\'t set the LD current ON')

    def test_starting_sweep(self):
        try:
            self.inst.execute_sweep()
        except:
            self.fail('Couldn\'t execute a wavelength sweep')

        self.assertEqual(self.inst.sweep_condition, 'Executing', 'Sweep is not executing')



if __name__ == '__main__':
    unittest.main()