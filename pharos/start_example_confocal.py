"""
    start_example_confocal
    ======================
    Example built by Sanli following Aquiles instructions on how to have a confocal scan without a GUI.
    Its main goal is as an educative project.
    @author: Sanli Faez
"""

from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.confocal import measurement

config_experiment = "config/example_confocal.yml"

experiment_dict = from_yaml_to_dict(config_experiment)
print(experiment_dict['GenWaveDetect']['axis'])
experiment = measurement(experiment_dict)

# start_logger('test.log')
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.gen_wave()
# experiment.connect_monitor_devices_to_daq()
# experiment.setup_scan()
# data_scan = experiment.do_scan()
# stop_logger()