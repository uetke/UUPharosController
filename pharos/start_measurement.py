
from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.measurement import measurement




config_experiment = "config/measurement.yml"

experiment_dict = from_yaml_to_dict(config_experiment)
print(experiment_dict['scan']['axis'])
experiment = measurement(experiment_dict)

# start_logger('test.log')
experiment.load_devices()  # Uses the file specified in the YAML
experiment.initialize_devices()
experiment.connect_all_devices_to_daq()
experiment.connect_monitor_devices_to_daq()
experiment.setup_scan()
data_scan = experiment.do_scan()
# stop_logger()