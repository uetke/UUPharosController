import unittest
import ctypes
import time
from time import sleep

from lantz import Q_

from pharos.controller.thorlabs.tdc001 import TDC


class TestThorlabs(unittest.TestCase):
    def setUp(self):
        try:
            self.inst = TDC(83860737)
        except:
            self.fail('Impossible to communicate with Thorlabs motor. Check the serial number.')

    def test_can_home(self):
        can_home = self.inst.can_home
        self.assertIsInstance(can_home, bool, 'can_home is not Bool')

    def test_dll(self):
        try:
            LIBRARY_NAME = 'Thorlabs.MotionControl.TCube.DCServo.DLL'
            filename = ctypes.util.find_library(LIBRARY_NAME)
            lib = ctypes.cdll.LoadLibrary(filename)
        except:
            self.fail('Couldn\'t find the Kinesis dll. Check the PATH!')

    def test_start_moving(self):
        self.inst.position = Q_('0deg')
        t0 = time.time()
        while not self.inst.finished_moving:
            sleep(1)
            if time.time - t0 > 60:
                self.fail('Timeout moving to 0 degrees')
        self.assertAlmostEqual(self.inst.position.m_as('deg'), 0, 'Position not 0 degrees')
        self.inst.position = Q_('10deg')
        while not self.inst.finished_moving:
            sleep(1)
            if time.time - t0 > 20:
                self.fail('Timeout moving to 10 degrees')
        self.assertAlmostEqual(self.inst.position.m_as('deg'), 10, 'Position not 10 degrees')


if __name__ == '__main__':
    unittest.main()