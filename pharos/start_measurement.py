"""
    start_measurement
    =================
    Starting point for a measurement without GUI. It is mainly an example of how things should be built from the ground
    up in order to later have a GUI.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""

from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.measurement import Measurement

config_experiment = "config/measurement.yml"

experiment_dict = from_yaml_to_dict(config_experiment)
print(experiment_dict['scan']['axis'])
experiment = Measurement(experiment_dict)

# start_logger('test.log')
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.connect_monitor_devices_to_daq()
experiment.setup_scan()
data_scan = experiment.do_scan()
# stop_logger()