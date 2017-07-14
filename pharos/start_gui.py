import sys
import yaml
from lantz import Q_
from model.lib.session import session
from model.lib.device import device
from PyQt4.Qt import QApplication
from view.main_window import MainWindow



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
        session.daq = DaqClass(daq_num=dev_num)
        for dev in devices[d]['devices']:
            dd = device(devices[d]['devices'][dev])
            print(dd.properties['limits'])
            session.daq_devices.append(dd)
    else:
        raise Warning('Work in progress')


def start_monitor(self, devs):
    """
    Starts the monitor on all the given devices
    """
    monitor_devices = []
    for dev in devs:
        if dev.properties['mode'] == 'input':
            monitor_devices.append(dev)

    conditions = {}
    conditions['devices'] = monitor_devices
    conditions['accuracy'] = 0.1
    conditions['trigger'] = 'external'


s = open('config/defaults.yml')
defaults = yaml.load(s)
s.close()
laser_defaults = defaults['tsl-710']
ap = QApplication(sys.argv)
with LaserClass.via_gpib(1) as session.laser:

    m = MainWindow(session)
    m.laser_widget.populate_values(laser_defaults)
    m.monitor_config_widget.populate_devices(session.daq_devices)
    m.show()
    ap.exit(ap.exec_())