import yaml
from model.lib.device import device

config_devices = "config/devices.yml"
config_experiment = "config/measurement.yml"

stream = open(config_devices, 'r')
devices = yaml.load(stream)['devices']
stream.close()

for d in devices:
    print(d)

stream = open(config_experiment, 'r')
experiment = yaml.load(stream)['steps']
stream.close()

for e in experiment:
    print(e)