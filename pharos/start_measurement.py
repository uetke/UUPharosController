
from pharos.model.lib.general_functions import from_yaml_to_dict, start_logger, stop_logger
from pharos.model.experiment.measurement import measurement




config_experiment = "config/measurement.yml"

experiment_dict = from_yaml_to_dict(config_experiment)
print(experiment_dict['scan']['axis'])
experiment = measurement(experiment_dict)

start_logger('test')
experiment.load_devices()  # Uses the file specified in the YAML
stop_logger()
experiment.initialize_devices()
experiment.do_scan()