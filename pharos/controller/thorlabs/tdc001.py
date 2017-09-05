import ctypes

from lantz.foreign import LibraryDriver

class TDC011(LibraryDriver):
    LIBRARY_NAME = 'Thorlabs.MotionControl.TCube.DCServo.DLL'

    def __init__(self, serial, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial = ctypes.c_char_p(serial.encode())