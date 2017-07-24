import yaml
import sys
from pharos.model.lib.session import session
from pharos.model.lib.device import device
from pharos.model.lib.general_functions import from_yaml_to_devices
from pharos.view.main_window import MainWindow
from PyQt4.Qt import QApplication
from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.measurement import measurement

config_devices = "config/devices.yml"

devs = from_yaml_to_devices(config_devices)
session = session()
session.daq_devices = []
session.devs_to_monitor = []


for dev in devs:
    if dev.properties['connection']['type'] == 'daq' and dev.properties['type'] != 'daq':
        session.daq_devices.append(dev)
        if dev.properties['mode'] == 'input':
            session.devs_to_monitor.append(dev)

s = open('config/devices_defaults.yml')
defaults = yaml.load(s)
s.close()
session.laser_defaults = defaults['Santec Laser']
ap = QApplication(sys.argv)
devs[0].initialize_driver()
session.laser = devs[0]
# session.daq = devs[4].driver

config_experiment = "config/measurement.yml"
experiment_dict = from_yaml_to_dict(config_experiment)
experiment = measurement(experiment_dict)
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.connect_monitor_devices_to_daq()

m = MainWindow(experiment)
m.show()
ap.exit(ap.exec_())