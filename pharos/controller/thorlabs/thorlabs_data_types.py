"""
    thorlabs_data_types
    ===================
    Defines the data structures needed for the devices used by Kinesis. They are broadly documented in
    the Kinesis installation folder, file Thorlabs.MotionControl.C_API.chm.
"""

import ctypes
import ctypes.util
from ctypes.wintypes import DWORD, WORD

class TLI_DeviceInfo(ctypes.Structure):
    """ Device info."""
    _fields_ = [('typeID', DWORD),
        ('description', ctypes.c_char*65), #type(ctypes.create_string_buffer(65))),
        ('serialNo', ctypes.c_char*9), #type(ctypes.create_string_buffer(9))),
        ('PID', DWORD),
        ('isKnownType', ctypes.c_bool),
        ('motorType', ctypes.c_int64),
        ('isPiezoDevice', ctypes.c_bool),
        ('isLaser', ctypes.c_bool),
        ('isCustomType', ctypes.c_bool),
        ('isRack', ctypes.c_bool),
        ('maxChannels', ctypes.c_short)]

class TLI_HardwareInformation(ctypes.Structure):
    _fields_ = [('serialNumber', DWORD),
                ('modelNumber', ctypes.c_char*8),
                ('type', WORD),
                ('numChannels', ctypes.c_short),
                ('notes', ctypes.c_char*48),
                ('firmwareVersion', DWORD),
                ('hardwareVersion', WORD),
                ('deviceDependantData', ctypes.c_byte*12),
                ('modificationState', WORD)]

class MOT_VelocityParameters(ctypes.Structure):
    _fields_ = [('minVelocity', ctypes.c_int),
                ('acceleration', ctypes.c_int),
                ('maxVelocity', ctypes.c_int)]

class MOT_JogParameters(ctypes.Structure):
    _fields_ = [('mode', ctypes.c_short),
                ('stepSize', ctypes.c_uint),
                ('velParams', MOT_VelocityParameters),
                ('stopMode', ctypes.c_short)]

class MOT_HomingParameters(ctypes.Structure):
    _fields_ = [('direction', ctypes.c_short),
                ('limitSwitch', ctypes.c_short),
                ('velocity', ctypes.c_uint),
                ('offsetDistance', ctypes.c_uint)]

class MOT_LimitSwitchParameters(ctypes.Structure):
    _fields_ = [('clockwiseHardwareLimit', WORD),
                ('anticlockwiseHardwareLimit', WORD),
                ('clockwisePosition', DWORD),
                ('anticlockwisePosition', DWORD),
                ('softLimitMode', WORD)]

class MOT_ButtonParameters(ctypes.Structure):
    _fields_ = [('buttonMode', WORD),
                ('leftButtonPosition', ctypes.c_int),
                ('rightButtonPosition', ctypes.c_int),
                ('timeout', WORD),
                ('unused', WORD)]

class MOT_PotentiometerStep(ctypes.Structure):
    _fields_ = [('thresholdDeflection', WORD),
                ('velocity', DWORD)]

class MOT_PotentiometerSteps(ctypes.Structure):
    _fields_ = [('potentiometerStepParameters', 4*MOT_PotentiometerStep)]

class MOT_DC_PIDParameters(ctypes.Structure):
    _fields_ = [('proportionalGain', ctypes.c_int),
                ('integralGain', ctypes.c_int),
                ('differentialGain', ctypes.c_int),
                ('integralLimit', ctypes.c_int),
                ('parameterFilter', WORD)]

import os
import time

os.environ['PATH'] = os.environ['PATH'] + ';' + 'C:\\Program Files (x86)\\Thorlabs\\Kinesis'
filename = ctypes.util.find_library("Thorlabs.MotionControl.TCube.DCServo.DLL")
lib = ctypes.cdll.LoadLibrary(filename)
serial = ctypes.c_char_p(b"83843619")

lib.CC_Open(serial)
lib.CC_ClearMessageQueue(serial)
lib.CC_EnableChannel(serial)
lib.CC_StartPolling(serial, 200)
lib.CC_LoadSettings(serial)
# lib.CC_MoveToPosition(serial, ctypes.c_int(0))
# dev_info = TLI_DeviceInfo()
# # dev_info.serialNo = serial
# print('DevInfo: {}'.format(lib.TLI_GetDeviceInfo(serial, ctypes.byref(dev_info))))
# print(dev_info.typeID)
# print('Needs Homing: {}'.format(lib.CC_CanMoveWithoutHomingFirst(serial)))
# lib.CC_Home(serial)
# stepsPerRev = ctypes.c_long()
# gearBoxRatio = ctypes.c_long()
# pitch = ctypes.c_float()
# lib.CC_GetMotorParams(serial, ctypes.byref(stepsPerRev), ctypes.byref(gearBoxRatio), ctypes.byref(pitch))
# print('Steps Per Rev: {}'.format(stepsPerRev.value))
# print('gearBoxRatio: {}'.format(gearBoxRatio.value))
# print('pitch: {}'.format(pitch.value))
# real_world = stepsPerRev.value*gearBoxRatio.value/pitch.value
# print('Real World Units: {}'.format(real_world))
# lib.CC_MoveToPosition(serial, ctypes.c_int(2147483647))

# vel_param = MOT_VelocityParameters()
# lib.CC_GetVelParamsBlock(serial, ctypes.byref(vel_param))
# print(lib.CC_GetNumberPositions(serial))
# messageType = WORD()
# messageID = WORD()
# messageData = DWORD()
# lib.CC_MoveToPosition(serial, ctypes.c_int(int(55*real_world)))
# time.sleep(0.5)
# q_size = lib.CC_MessageQueueSize(serial)
# print('Message Queue Size: {}'.format(q_size))
# for _ in range(q_size):
#     lib.CC_GetNextMessage(serial, ctypes.byref(messageType), ctypes.byref(messageID), ctypes.byref(messageData))
#     print(10*'=')
#     print(messageType)
#     print(messageID.value)
#     print(messageData)
#
# hdw = TLI_HardwareInformation()
# lib.CC_GetHardwareInfoBlock(serial, ctypes.byref(hdw))
#
# print(hdw.notes)

real_world = 1900
lib.CC_MoveToPosition(serial, ctypes.c_int(int(55*real_world)))
# lib.CC_Home(serial)