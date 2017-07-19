import yaml
from pharos.model.lib.general_functions import from_yaml_to_devices, from_yaml_to_experiment

config_devices = "config/devices.yml"
config_experiment = "config/measurement.yml"

devices = from_yaml_to_devices(config_devices)
experiment = from_yaml_to_experiment(config_experiment)

for e in experiment:
    print(e)
    print(experiment[e])