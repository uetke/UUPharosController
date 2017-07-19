from pharos.model.lib.session import session
from pharos.model.lib.device import device
from pharos.model.lib.general_functions import from_yaml_to_devices
from pharos.view.main_window import MainWindow
from PyQt4.Qt import QApplication


config_devices = "config/devices.yml"

devs = from_yaml_to_devices(config_devices)
session = session()
session.daq_devices = []
session.devs_to_monitor = []


for dev in devs:
    if dev['connection']['type'] == 'daq':
        session.daq_devices.append(dev)
        if dev['mode'] == 'input':
            session.devs_to_monitor.append(dev)

s = open('config/devices_defaults.yml')
defaults = yaml.load(s)
s.close()
session.laser_defaults = defaults['tsl-710']
ap = QApplication(sys.argv)
with LaserClass.via_gpib(1) as session.laser:

    m = MainWindow(session)
    m.show()
    ap.exit(ap.exec_())