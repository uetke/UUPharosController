import sys
import yaml
from pprint import pprint
from model.lib.session import session
from model.lib.device import device
from view.main_window import MainWindow
from PyQt4.Qt import QApplication


config_devices = "config/devices.yml"

stream = open(config_devices, 'r')
devices = yaml.load(stream)['devices']
stream.close()

devs = []
session = session()
session.daq_devices = []

for d in devices:
    if devices[d]['type'] == 'laser':
        if devices[d]['model'] == 'santec':
            from controller.santec.tsl710 import tsl710 as LaserClass
        else:
            raise Exception('Model for %s is not implemented' % devices[d])
        session.laser = None
        # port = devices[d]['connection']['port']
        # print(type(port))
        # connection_type = devices[d]['connection']['type']
        # if connection_type == 'GPIB':
        #     session.laser = LaserClass.via_gpib(port)
        # elif connection_type == 'USB':
        #     session.laser = LaserClass.via_usb(port)
        # elif connection_type == 'SERIAL':
        #     session.laser = LaserClass.via_serial(port)
        # else:
        #     raise Exception('Connection type not specified for the laser.')

    elif devices[d]['type'] == 'daq':
        if devices[d]['model'] == 'ni':
            from model.daq.ni import ni as DaqClass
        else:
            raise Exception('Model for %s is not implemented' % devices[d])

        dev_num = devices[d]['number']
        #session.daq = DaqClass(device_number=dev_num)
        session.daq = None
        inp = devices[d]['ports']['input']
        for p in inp:
            session.daq_devices.append(device(inp[p]))
            session.daq_devices[-1].type = 'input'

        out = devices[d]['ports']['input']
        for p in out:
            session.daq_devices.append(device(inp[p]))
            session.daq_devices[-1].type = 'output'
    else:
        raise Warning('Work in progress')

s = open('config/defaults.yml')
defaults = yaml.load(s)
s.close()
laser = defaults['tsl-710']
ap = QApplication(sys.argv)
m = MainWindow(session)
m.laser_widget.populate_values(laser)
m.show()
ap.exit(ap.exec_())