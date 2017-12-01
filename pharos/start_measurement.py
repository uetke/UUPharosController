"""
    start_measurement
    =================
    Starting point for a measurement without GUI. It is mainly an example of how things should be built from the ground
    up in order to later have a GUI.

    .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
from time import sleep
from lantz import Q_

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
experiment.sync_shutter()
experiment.scan['laser']['params'].update({
    'start_wavelength': Q_(experiment.scan['laser']['params']['start_wavelength']),
    'stop_wavelength': Q_(experiment.scan['laser']['params']['stop_wavelength']),
    'wavelength_speed': Q_(experiment.scan['laser']['params']['wavelength_speed']),
    'interval_trigger': Q_(experiment.scan['laser']['params']['interval_trigger']),
    'wavelength_sweeps': Q_(experiment.scan['laser']['params']['wavelength_sweeps']),
})

experiment.wait_for_line = True # True for reading data after each line (and accumulates into scan_data property
experiment.scan['sampling'] = 'finite' # Sets the behavior of the DAQ. 'finite'/'continuous' acquisition mode.
experiment.setup_scan()
experiment.do_scan()

### READ ALL THE DATA ###
data_scan = experiment.scan_data
for i in range(len(data_scan)):
    data = data_scan[i]
    for d in data:
        print('Length of {}: {}'.format(d,len(data[d])))
        
experiment.save_data(data_scan, 'F:\\Data\\test.dat')